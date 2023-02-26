'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: select_articles.py
Associated files: export.py, process_articles.py
Primary Author: Kathryn Link-Oberstar
Addiditional Authors: None

Description: Search through a list of article dictionaries using candidate name
tokens and assign articles to a candidate if their name appears in that article.
Export these dictionaries as 
'''
import os
import sys
import re
import json
import pandas as pd
from process_articles import convert_to_dict

#Strings to file paths - Run function once for each paper
#Chicago Tribune
#PROQUEST_FILES = [('chicago_tribune_2022.tar', 'data/chicago_tribune_2022.parquet'), 
#                ('chicago_tribune_2023.tar', 'data/chicago_tribune_2023.parquet')]
#NEWSPAPER_ID = "news_ct"
#JSON_FILEPATH = '/data/chicago_tribune.json'

#Crain Business
PROQUEST_FILES = [('crain.tar', 'data/crain.parquet')]
NEWSPAPER_ID = "news_cc"
JSON_FILEPATH = '/data/crain.json'

# Import Search Strings Function to retrieve candidate names from database
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
grandparent = os.path.dirname(parent)
sys.path.append(grandparent)
from utilities.data_retrieval import search_strings


# Pull Candidiate Name tokens from database and put into a dictionary
search_strings = search_strings(newspaper_id = 'news_ct')
cand_name_dict = (search_strings.groupby('candidate_id')['name_tokens']
                    .apply(lambda x: list(set(x)))
                    .to_dict())

def article_selection(PROQUEST_FILES, NEWSPAPER_ID):
    '''
    Search list of dictionaries of articiles and find all mention.
    '''
    all_articles = []

    for file in PROQUEST_FILES:
        tar, parquet = file
        articles = convert_to_dict(tar, parquet, NEWSPAPER_ID)
        all_articles += articles
    
    cand_ids = search_strings['candidate_id'].unique()
    cand_articles = {val: [] for val in cand_ids}

    for article in all_articles:
        for cand_id, names in cand_name_dict.items():
            for name in names:
                if re.search(name, article['Text']):
                    article['candidate_id'] = cand_id
                    article['name_tokens'] = name
                    article['announcement_date'] = search_strings.loc[search_strings['candidate_id'] == cand_id,'announcement_date'].iloc[0]
                    article['Newspaper_id'] = NEWSPAPER_ID
                    cand_articles[cand_id].append(article)
                    break

    return cand_articles

def export_jsons(PROQUEST_FILES, NEWSPAPER_ID):
    all_articles = []
    article_dict = article_selection(PROQUEST_FILES, NEWSPAPER_ID)
    for articles in article_dict.values():
        all_articles += articles
    
    print("Writing json")
    filepath = sys.path[-2] + JSON_FILEPATH
    with open(filepath, "w") as f:
        json.dump(all_articles, f, indent=1)   


