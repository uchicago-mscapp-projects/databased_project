"""
Project: CAPP 122 DataBased Project
File name: bag_of_words.py

Finds and the most frequent words associated with a candidates and newspapers.

@Author: Madeleine Roberts
@Date: Mar 2, 2023
"""
import nltk
#nltk.download("stopwords")
#nltk.download('vader_lexicon')
import sys
import os
import pandas as pd
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from most_frequent_words import single_text_str


def basic_sentence_sentiment():
    df = pd.read_json('data/clean_articles.json')
    sia = SentimentIntensityAnalyzer()

    cand_sentiment = sentence_sentiment_single_token(sia, df, "candidate_id", "clean_sentences")
    news_sentiment = sentence_sentiment_single_token(sia, df, "newspaper_id", "clean_text")
    cand_by_newspaper_sentiment = sentence_sentiment_cand_by_news(sia, df)

    return cand_sentiment, news_sentiment, cand_by_newspaper_sentiment
    

def sentence_sentiment_single_token(sia, df, token, text_to_inspect):
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