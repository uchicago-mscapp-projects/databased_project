"""
Project: CAPP 122 DataBased Project
File name: most_frequent_words.py

Finds and the most frequent words associated with a candidates and newspapers.

@Author: Madeleine Roberts
@Date: Mar 1, 2023
"""
# python3 -m pip install nltk
# nltk.download("stopwords")
import nltk
import pandas as pd
import json
import os
import sys
from nltk.corpus import stopwords
from collections import Counter

#from basic_sentiment import write_to_json

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings

def most_frequent():
    """
    Reads in a JSON file containing cleaned article data (change), and calculates 
    the most frequent words in the text data for each candidate and each newspaper source, 
    as well as the most frequent words overall for candidates within newspapers.

    Returns
        Tuple containing:
            A dictionary corrisponding to the most frequent words in the text data for each candidate
            A dictionary corrisponding to the most frequent words in the text data for each newspaper
            A dictionary corrisponding to the most frequent words in the text data for each candidates within newspapers
    """
    # will probably have to read in as data base
    df = pd.read_json('data/clean_articles.json')
    
    # Additional words that should not be included in the most frequent word count
    cand_stopwords = ['kambium', 'elijah', 'kam', 'buckner', 'jesús', 'jesus',
        'chuy', 'garcía', 'garcia', 'ja', 'mal', 'green', 'jamal', 'sophia', 'king',
        'roderick', 'sawyer', 'paul', 'vallas', 'willie', 'wilson', 'lori',
        'lightfoot', 'johnson', 'brandon', 'paul', 'buckner', 'said', 'also', 'would',
        'city', 'former', '.']

    news_stopwords = ['said', 'also', 'would', 'city', 'former', '.']
    
    cand_word_freq = calc_most_frequent_single(df, "candidate_id", cand_stopwords, "clean_sentences")
    write_to_json("candidate_word_freq.json", cand_word_freq)

    news_word_freq = calc_most_frequent_single(df, "newspaper_id", news_stopwords, "clean_text")
    write_to_json("news_word_freq.json", news_word_freq)

    cand_by_news_freq = calc_most_frequent_double(df, cand_stopwords)
    write_to_json("cand_by_news_freq.json", cand_by_news_freq)

    #return cand_word_freq, news_word_freq, cand_by_news_freq

def calc_most_frequent_single(df, token, additional_stop_words, text_to_inspect):
    """
    Calculates the most frequent words in the text data for token.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing data for token.
        additional_stop_words (list): A list of additional stop words to filter out.

    Returns
        A dictionary with the keys corresponding to the token and associated value is a
        list of tuples, where each tuple contains a word and its frequency count, after filtering out 
        stop words. This frequency list contains the about 50 most common words in the text data for that token. 
    """
    unique_ids = df.loc[:,[token]].drop_duplicates()
    list_ids = unique_ids[token].values.tolist()

    respective_word_dict = {}

    for identifier in list_ids:
        subset = df.loc[df[token] == identifier]
     
        # Concatenate all pretaining text into one string
        full_text = single_text_str (subset, text_to_inspect)

        # Find frequency of words in text and recover top 100
        words = Counter()
        words.update(full_text.split())
        most_common = words.most_common(100)

        # Find ~50 top words when excluding stop words from count
        freq_list = calc_freq(most_common, additional_stop_words)
        
        respective_word_dict[identifier] = freq_list

    return respective_word_dict

def calc_most_frequent_double(df, additional_stop_words):
    """
    Calculates the most frequent words in the text data for each candidate and each newspaper source.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing data for each candidate and newspaper source.
        additional_stop_words (list): A list of additional stop words to filter out.

    Returns
        A double dictionary with the first level of keys corresponds to the newspaper source ID, 
        and the second level of keys corresponds to the candidate ID. The value associated with each second-level 
        key is a list of tuples, where each tuple contains a word and its frequency count, after filtering out 
        stop words. This frequency list contains the about 50 most common words in the text data for that candidate 
        and newspaper source.
    """
    news_ids = df.loc[:,["newspaper_id"]].drop_duplicates()
    list_news_ids = news_ids["newspaper_id"].values.tolist()

    complete_dict = {}

    # iterate over newspapers
    for news_source in list_news_ids:
        news_dict = {}
       
        cand_ids = df.loc[:,["candidate_id"]].drop_duplicates()
        list_cand_ids = cand_ids["candidate_id"].values.tolist()
        subset = df.loc[df["newspaper_id"] == news_source]

        # calculate the frequency for each candidate within the news paper
        complete_dict[news_source] = calc_most_frequent_single(subset, "candidate_id", additional_stop_words, "clean_sentences")

    return complete_dict

def single_text_str (df, text_to_inspect):
    """
    Concatenates all text values in the given DataFrame column into a single string.

    Parameters:
        * df (pandas.DataFrame): The DataFrame containing the text data to concatenate.
        * text_to_inspect (str): The name of the column containing the text data to concatenate.

    Returns:
        A single string that is the concatenation of all text values in the specified column.
    """
    full_text = ""
    for __, row in df.iterrows():
        full_text += row[text_to_inspect]
        full_text += " "
    
    return full_text

def calc_freq(most_common, additional_stop_words):
    """
    Calculates the frequency list of words after filtering out stop words.

    Parameters:
        * most_common (list): A list of 100 tuples, where each tuple contains a word and its frequency count.
    additional_stop_words : List[str]
        A list of additional stop words to filter out.
    """
    freq_list = []
    stop_words = (stopwords.words('english'))
    stop_words.extend(additional_stop_words)

    for word_freq in most_common:
        word, freq = word_freq
        if word  not in  stop_words:
            freq_list.append(word_freq)

    return freq_list

def write_to_json(file_name, sentiment_data):
    """
    Writes the given dictionary of sentiment data to a JSON file with the given file name.

    Parameters:
        * file_name (str): The name of the JSON file to write to
        * sentiment_data (dict): The dictionary of sentiment data to write to the JSON file.
    """
    print("Writing to json")
    filepath = sys.path[-1] + '/data/' + file_name

    with open(filepath, "w") as f:
        json.dump(sentiment_data, f, indent=1)

    
if __name__ == "__main__":
    most_frequent()



    