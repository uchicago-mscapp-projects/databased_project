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
from analysis_helpers import single_text_str, write_to_json, unique_list

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
    write_to_json("word_freq_candidate.json", cand_word_freq)

    news_word_freq = calc_most_frequent_single(df, "newspaper_id", news_stopwords, "clean_text")
    write_to_json("word_freq_news.json", news_word_freq)

    cand_by_news_freq = calc_most_frequent_double(df, cand_stopwords)
    write_to_json("word_freq_cand_by_news.json", cand_by_news_freq)

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
    list_ids = unique_list(df, token)
   
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
    list_news_ids = unique_list(df, "newspaper_id")
    
    complete_dict = {}

    # iterate over newspapers
    for news_source in list_news_ids:
        news_dict = {}
       
        subset = df.loc[df["newspaper_id"] == news_source]

        # calculate the frequency for each candidate within the news paper
        complete_dict[news_source] = calc_most_frequent_single(subset, "candidate_id", additional_stop_words, "clean_sentences")

    return complete_dict

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
 
if __name__ == "__main__":
    most_frequent()



    