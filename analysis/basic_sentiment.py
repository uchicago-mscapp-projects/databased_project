"""
Project: CAPP 122 DataBased Project
File name: bag_of_words.py

Finds and the most frequent words associated with a candidates and newspapers.

@Author: Madeleine Roberts
@Date: Mar 2, 2023
"""
import nltk
#nltk.download("stopwords")
#nltk.download("opinion")
nltk.download('vader_lexicon')
import sys
import os
import pandas as pd
from nltk.corpus import stopwords
#from nltk.corpus import opnion
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings

def basic_sentence_sentiment():
    df = pd.read_json('data/clean_articles.json')
    sia = SentimentIntensityAnalyzer()

    # will probably have to read in as data base
    df = pd.read_json('data/clean_articles.json')
    

    df = pd.read_json('data/clean_articles.json')

if __name__ == "__main__":
    basic_sentence_sentiment()