import nltk
#nltk.download("stopwords")
#nltk.download('vader_lexicon')
import sys
import os
import json
import pandas as pd
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from most_frequent_words import single_text_str

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings

def basic_bag_of_words():
    # Training data: change this
    
    df = pd.read_json('data/clean_articles.json')