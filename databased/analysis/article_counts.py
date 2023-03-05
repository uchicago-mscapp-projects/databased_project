"""
Project: CAPP 122 DataBased Project
File name: article_counts.py

Finds the scraped article counts for candidates, newspapers, and candidates by
newspaper.

@Author: Madeleine Roberts
@Date: Mar 1, 2023
"""

import sys
import os
import json
import pandas as pd
from .analysis_helpers import write_to_json, unique_list

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings


def retrieve_total_article_counts():
    """
    Reads in a JSON file of cleaned articles and calculates various article counts. 
    Calculates the total number of articles, the number of unique articles, 
    and the number of articles for each newspaper and candidate.
    Writes the article counts to separate JSON files.
    """

    df = pd.read_json('databased/data/clean_articles.json')

    dataframe_size = len(df)
    unique_art_count = len(df.loc[:,["url"]].drop_duplicates())

    count_by_news = single_counter(df, "newspaper_id")
    postprocess(count_by_news, dataframe_size, unique_art_count)
    write_to_json("count_news.json", count_by_news)
    
    count_by_cand = single_counter(df, "candidate_id")
    postprocess(count_by_cand, dataframe_size, unique_art_count)
    write_to_json("count_cand.json", count_by_cand)
    
    count_cand_by_news = cand_by_news_counter(df)
    postprocess(count_cand_by_news, dataframe_size, unique_art_count)
    write_to_json("count_cand_by_news.json", count_cand_by_news)
   
    
def single_counter(df, token):
    """
    Computes the article counts with respect to each unique identifier token in a dataframe.

    Parameters:
        * df (pandas.DataFrame): A dataframe containing the article data to be counted.
        * token (str): The column name of the unique identifier token in the dataframe.

    Returns:
       A dictionary containing the respective counts for each unique identifier token in the dataframe
    """

    if token == "newspaper_id":
        df = df.drop_duplicates("url")

    list_ids = unique_list(df, token)

    token_dict = {}

    for identifier in list_ids:

        subset = (df.loc[df[token] == identifier])
        if token == "candidate_id":
            subset = subset.drop_duplicates("url")
     
        token_dict[identifier] = len(subset)

    return token_dict

def cand_by_news_counter(df):
    """
    Computes the article counts for each candidate within each newspaper.

    Parameters:
        * df (pandas.DataFrame): A dataframe containing the article data to be counted.

    Returns:
       A dictionary containing dictionaries for each newspaper where the values are 
       the respective article counts for each candidate within the respective newspaper.
    """

    list_news_ids = unique_list(df, "newspaper_id")

    complete_dict = {}

    for news_source in list_news_ids:
        news_dict = {}
        
        subset = df.loc[df["newspaper_id"] == news_source]
        complete_dict[news_source] = single_counter(subset, "candidate_id")
        
    return complete_dict

def postprocess(count_dict, total_articles, total_unique_articles):
    """
    Updates a dictionary containing counts of articles scraped, by adding two 
    additional keys to the dictionary representing the total number of articles 
    scraped and the total number of unique articles scraped.

    Parameters:
        * count_dict (dict): A dictionary containing counts of articles scraped
        * total_articles (int): The total number of articles scraped
        * total_unique_articles (int): The total number of unique articles scraped

    """
    count_dict["total_num_articles_scraped"] = total_articles
    count_dict["total_unique_articles_scraped"] = total_unique_articles

if __name__ == "__main__":
    retrieve_total_article_counts()