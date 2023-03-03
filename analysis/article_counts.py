import sys
import os
import json
import pandas as pd
from analysis_helpers import write_to_json, unique_list

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings


def retrieve_total_article_counts():
    df = pd.read_json('data/clean_articles.json')

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
    if token == "newspaper_id":
        df = df.drop_duplicates("url")

    list_ids = unique_list(df, token)

    token_dict = {}

    for identifier in list_ids:

        subset = (df.loc[df[token] == identifier])
        if token == "candidate_id":
            subset = subset.drop_duplicates("url")
     
        # Concatenate all pretaining text into one string
        token_dict[identifier] = len(subset)

    return token_dict

def cand_by_news_counter(df):
    list_news_ids = unique_list(df, "newspaper_id")

    complete_dict = {}

    for news_source in list_news_ids:
        news_dict = {}
        
        subset = df.loc[df["newspaper_id"] == news_source]
        complete_dict[news_source] = single_counter(subset, "candidate_id")
        
    return complete_dict

def postprocess(count_dict, total_articles, total_unique_articles):
    count_dict["total_num_articles_scraped"] = total_articles
    count_dict["total_unique_articles_scraped"] = total_unique_articles

if __name__ == "__main__":
    retrieve_total_article_counts()