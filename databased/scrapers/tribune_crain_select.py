'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: tribune_crain_select.py
Associated files: tribune_crain_process.py
Author: Kathryn Link-Oberstar

Description: Search through a list of article dictionaries using candidate name
tokens and assign articles to a candidate if their name appears in that article.
Export these dictionaries as a list of JSONs.
'''
#!python3 pip install pyarrow
import os
import sys
import re
import json
from copy import deepcopy

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings
from scrapers.tribune_crain_process import convert_to_dict

TRIBUNE_FILEPATHS = ([(sys.path[-1] + '/data/proquest_files/chicago_tribune_2022.tar',
                'data/chicago_tribune_2022.parquet', 1000),
                (sys.path[-1] + '/data/proquest_files/chicago_tribune_2023.tar',
                'data/chicago_tribune_2023.parquet', 3000),
                (sys.path[-1] + '/data/proquest_files/chicago_tribune_final.tar',
                'data/chicago_tribune_final.parquet', 5000)],
                "news_ct",'/data/chicago_tribune.json')
CRAIN_FILEPATHS = ([(sys.path[-1] + '/data/proquest_files/crain.tar',
            'data/crain.parquet', 7000)], "news_cc", '/data/crain.json')

def run_selection():
    """
    Search through a list of article dictionaries using candidate name tokens
    and assign articles to a candidate if their name appears in that article.
    Export these dictionaries as a list of JSONs.

    The function loops through two lists of newspaper files ('TRIBUNE_FILEPATHS'
    and 'CRAIN_FILEPATHS'), and for each newspaper, it calls the
    'export_jsons' function to process the articles and write them to a JSON
    file.

    Inputs:
        None

    Outputs:
        None. Writes JSON file of selected articles to the data folder
    """
    papers = [TRIBUNE_FILEPATHS, CRAIN_FILEPATHS]
    for paper in papers:
        proquest_files, newspaper_id, json_filepath = paper
        export_jsons(proquest_files, newspaper_id, json_filepath)

def article_selection(proquest_files, newspaper_id):
    '''
    Search list of dictionaries of articles and find all mentions of a specific
    candidate. If the candidate is mentioned in an article, append that article
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
    search_str = search_strings(newspaper_id = newspaper_id)
    cand_name_dict = (search_str.groupby('candidate_id')['name_tokens']
                    .apply(lambda x: list(set(x)))
                    .to_dict())
    cand_name_dict["cand_jg"] += ['JaMal Green']

    all_articles = []
    for file in proquest_files:
        tar, parquet, url_counter = file
        articles = convert_to_dict(tar, parquet, newspaper_id, url_counter)
        all_articles += articles

    cand_ids = search_str['candidate_id'].unique()
    cand_articles = {val: [] for val in cand_ids}

    for article in all_articles:
        for cand_id, names in cand_name_dict.items():
            for name in names:
                if re.search(name, article['text']):
                    article_copy = deepcopy(article)
                    article_copy['candidate_id'] = cand_id
                    article_copy['name_tokens'] = name
                    article_copy['announcement_date'] = \
                    search_str.loc[search_str['candidate_id']
                                    == cand_id,'announcement_date'].iloc[0]
                    article_copy['newspaper_id'] = newspaper_id
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

if __name__ == "__main__":
    run_selection()
