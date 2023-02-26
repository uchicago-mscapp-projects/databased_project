'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: proquest_process.py
Associated files: proquest_export.py
Primary Author: Kathryn Link-Oberstar
Addiditional Authors: None

Description: 

Purpose: 
'''
#from ..utilities.data_retrieval import query
import os
import sys
import re
import tarfile
import json
import pandas as pd

# Import helper functions to call from database
current = os.path.dirname(os.path.realpath(__file__)) 
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings

STRINGS_TO_REMOVE = ["<meta name='ValidationSchema' content='http://www.w3.org/2002/08/xhtml/xhtml1-strict.xsd'/>",
"</i>", "</p>", "</body>", "</html>", "<head>", "<title>", "</title>", 
"</head>", "<body>", "<p>", "<html>", "<b>", "<i>", "</b>", "\n"]

#List of strings to file path

# Chicago Tribune
PROQUEST_FILES = [('chicago_tribune_2022.tar', 'data/chicago_tribune_2022.parquet'), 
                  ('chicago_tribune_2023.tar', 'data/chicago_tribune_2023.parquet')]
SITE_ID = "news_ct"

# Crain Business
#PROQUEST_FILES = [('crain.tar', 'data/crain.parquet')]
#SITE_ID = "news_cc"




#Pull Candidiate Name tokens from database and put into a dictionary
cand_name_dict = {'cand_kb': ["Kam Buckner", "Kambium “Kam” Buckner"], 
             'cand_cg': ["‘Chuy’ García", "Jesús “Chuy” García", "Chuy Garcia"]}

def article_selection(PROQUEST_FILES, SITE_ID):
    '''
    Search list of dictionaries of articiles and find all mention 
    '''
    all_articles = []

    for file in PROQUEST_FILES:
        tar, parquet = file
        articles = convert_to_dict(tar, parquet, SITE_ID)
        all_articles += articles
    
    # Maybe do from DB
    cand_articles = {'cand_kb': [], 'cand_cg': []}

    for article in all_articles:
        for cand_id, names in cand_name_dict.items():
            for name in names:
                if re.search(name, article['Text']):
                    article['Candidate ID'] = cand_id
                    article['Associated Candidate'] = name
                    article['Search Field'] = f"{name} mayor"
                    cand_articles[cand_id].append(article)
    #print("cand_articles", cand_articles)
    return cand_articles

def unpack_file(tar, parquet):
    tz_file = tarfile.open(tar)
    parquet_file = tz_file.extractall("./")
    parquet_file = tz_file.extractfile(parquet)
    df_jsons = pd.read_parquet(parquet_file)
    tz_file.close()
    return df_jsons

def convert_to_dict(tar, parquet, site_id):
    url_counter = 0
    df_jsons = unpack_file(tar, parquet)
    all_results = []
    for row in df_jsons.iterrows():
        url_counter += 1
        row_json = json.loads(row[1]['Data'])
        website_title = row_json["RECORD"]["DFS"]['PubFrosting']['Title']
        text = row_json["RECORD"]["TextInfo"]['Text']['#text']
        text_clean= re.sub('|'.join(STRINGS_TO_REMOVE), '', text)
        url = url_counter
        seach_field = None
        title = row_json["RECORD"]['Obj']['TitleAtt']['Title']
        pub_date = row_json["RECORD"]['Obj']['NumericDate']
        tags = None
        site_ID = site_id
        cand_ID = None
        result_dict = {'Website Title': website_title, "URL": url, 
                    'Search Field': seach_field, 'Title': title, 
                    'Text': text_clean, 'Associated Candidate': None, 
                    'Publication Date' : pub_date, 'Tags' : tags, 
                    'Site ID' : site_ID, 'Candidate ID' : cand_ID}
        all_results.append(result_dict)
    return all_results

article_selection(PROQUEST_FILES, SITE_ID)