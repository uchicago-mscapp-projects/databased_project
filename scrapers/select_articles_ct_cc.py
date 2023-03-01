'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: select_articles.py
Associated files: process_articles_ct_cc.py
Primary Author: Kathryn Link-Oberstar
Addiditional Authors: None

Description: Search through a list of article dictionaries using candidate name
tokens and assign articles to a candidate if their name appears in that article.
Export these dictionaries as a list of JSONs.
'''
import os
import sys
import re
import json
import pandas as pd
from copy import deepcopy
from process_articles_ct_cc import convert_to_dict

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings

#Strings to file paths - Run function once for each paper
#Chicago Tribune
proquest_files = [(sys.path[-1] + '/data/proquest_files/chicago_tribune_2022.tar', 
                   'data/chicago_tribune_2022.parquet'), 
                (sys.path[-1] + '/data/proquest_files/chicago_tribune_2023.tar', 
                 'data/chicago_tribune_2023.parquet')]
newspaper_id = "news_ct"
json_filepath = '/data/chicago_tribune.json'

#Crain Business
proquest_files = [(sys.path[-1] + '/data/proquest_files/crain.tar', 
                   'data/crain.parquet')]
newspaper_id = "news_cc"
json_filepath = '/data/crain.json'

def article_selection(proquest_files, newspaper_id):
    '''
    Search list of dictionaries of articles and find all mentions of a specific 
    candidate. If the candidate is mentioned in an article, append that artice 
    to a list of articles for that candidate. The article lists are storted in 
    a dictionary where the key is the candidate ID, and the value is a list
    of dictionaries, one for each article. The values for 'candidate_id', 
    'name_tokens', 'announcement_date' within the article dictionary will also 
    be updated at this stage from None to the correct value.

    Inputs:
        proquest_files (tuple of strings): tuple of strings with the tar
            file path and the parquet file path
        newspaper_id (string): Unique ID for the newspaper being analyzed
    Output:
        df_jsons (pandas dataframe): pandas dataframe of JSON files, where 
            each file is an article
    '''
    search_strings = search_strings(newspaper_id = newspaper_id)
    cand_name_dict = (search_strings.groupby('candidate_id')['name_tokens']
                    .apply(lambda x: list(set(x)))
                    .to_dict())
    
    all_articles = []
    for file in proquest_files:
        tar, parquet = file
        articles = convert_to_dict(tar, parquet, newspaper_id)
        all_articles += articles
    
    cand_ids = search_strings['candidate_id'].unique()
    cand_articles = {val: [] for val in cand_ids}

    for article in all_articles:
        for cand_id, names in cand_name_dict.items():
            for name in names:
                if re.search(name, article['Text']):
                    article_copy = deepcopy(article)
                    article_copy['candidate_id'] = cand_id
                    article_copy['name_tokens'] = name
                    article_copy['announcement_date'] = \
                    search_strings.loc[search_strings['candidate_id'] 
                                    == cand_id,'announcement_date'].iloc[0]
                    article_copy['Newspaper_id'] = newspaper_id
                    cand_articles[cand_id].append(article_copy)
                    break
    return cand_articles

def export_jsons(proquest_files, newspaper_id, json_filepath):
    '''
    Export lists of articles to JSON filtes in the data directory. 
    
    Inputs:
        proquest_files (list of tuples of strings): tuple of strings with the 
            tar file path and the parquet file path
        newspaper_id (string): Unique ID for the newspaper being analyzed
        json_filepath  (strong): file path to the JSON file to export
    
    Output:
       Function writes list of JSON files to a JSON file in data director
    '''
    all_articles = []
    article_dict = article_selection(proquest_files, newspaper_id)
    for articles in article_dict.values():
        all_articles += articles
    
    print("Writing json")
    filepath = sys.path[-1] + json_filepath 
    with open(filepath, "w") as f:
        json.dump(all_articles, f, indent=1)   


