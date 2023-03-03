"""
Project: CAPP 122 DataBased Project
File name: basic_sentiment.py

Finds the basic sentiment of articles about candidates and within newspapers by
using NLTK’s built-in classifier, which uses VADER.

NOTE: running this file takes about 10 minutes

@Author: Madeleine Roberts
@Date: Mar 2, 2023
"""
import nltk
#nltk.download("stopwords")
#nltk.download('vader_lexicon')
import sys
import os
import json
import pandas as pd
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from analysis_helpers import single_text_str, write_to_json

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings


def basic_sentence_sentiment():
    """
    Computes sentiment scores for the candidate, newspaper, and candidate by newspaper pairs.

    Returns:
        A tuple containing three dictionaries. 
        - The first dictionary contains the sentiment scores for each candidate. 
        - The second dictionary contains the sentiment scores for each newspaper. 
        - The third dictionary contains the respective sentiment scores for each unique candidate-newspaper pair.
    
    """
    df = pd.read_json('data/clean_articles.json')
    sia = SentimentIntensityAnalyzer()

    # cand_sentiment takes about 30 seconds to calculate
    cand_sentiment = sentence_sentiment_single_token(sia, df, "candidate_id", "clean_sentences")
    write_to_json("candidate_bs.json", cand_sentiment)
    
    # cand_by_newspaper_sentiment takes about 30 seconds
    cand_by_newspaper_sentiment = sentence_sentiment_cand_by_news(sia, df)
    write_to_json("cand_by_newspaper_bs.json", cand_by_newspaper_sentiment)

    # news_sentiment takes about 20 minutes
    news_sentiment = sentence_sentiment_single_token(sia, df, "newspaper_id", "clean_text")
    write_to_json("news_bs.json", news_sentiment)


def sentence_sentiment_single_token(sia, df, token, text_to_inspect):
    """
    Computes the sentiment scores for a given text with respect to each unique 
    identifier token in a dataframe.

    Parameters:
        * sia (SentimentIntensityAnalyzer): An instance of SentimentIntensityAnalyzer.
        * df (pandas.DataFrame): A dataframe containing the text data to be analyzed.
        * token (str): The column name of the unique identifier token in the dataframe.
        * text_to_inspect (str): The column name of the text data to be analyzed in the dataframe.

    Returns:
       A dictionary containing the respective sentiment scores for each unique identifier token in the dataframe
    """
    unique_ids = df.loc[:,[token]].drop_duplicates()
    list_ids = unique_ids[token].values.tolist()

    respective_word_dict = {}

    for identifier in list_ids:

        subset = df.loc[df[token] == identifier]
     
        # Concatenate all pretaining text into one string
        full_text = single_text_str (subset, text_to_inspect)
        respective_word_dict[identifier] = sia.polarity_scores(full_text)

    return respective_word_dict


def sentence_sentiment_cand_by_news(sia, df):
    """
    Computes the sentiment scores for each candidate within each newspaper.

    Parameters:
        * sia (SentimentIntensityAnalyzer): An instance of SentimentIntensityAnalyzer.
        * df (pandas.DataFrame): A dataframe containing the text data to be analyzed.

    Returns:
       A dictionary containing dictionaries for each newspaper where the values are 
       the respective sentiment scores for each candidate within the respective newspaper.
    """
    news_ids = df.loc[:,["newspaper_id"]].drop_duplicates()
    list_news_ids = news_ids["newspaper_id"].values.tolist()

    complete_dict = {}

    for news_source in list_news_ids:
        news_dict = {}
        
        cand_ids = df.loc[:,["candidate_id"]].drop_duplicates()
        list_cand_ids = cand_ids["candidate_id"].values.tolist()
        subset = df.loc[df["newspaper_id"] == news_source]

        complete_dict[news_source] = sentence_sentiment_single_token(sia, subset, "candidate_id", "clean_sentences")
    return complete_dict


if __name__ == "__main__":
    basic_sentence_sentiment()