'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: tribune_crain_process.py
Associated files: tribune_crain_select.py
Primary Author: Kathryn Link-Oberstar

Description: Decompress Proquest Data Files, and process articles to create a
list of dictionaries, one for each article.
'''
import sys
import re
import tarfile
import json
import pandas as pd

STRINGS_TO_REMOVE = ["<meta name='ValidationSchema' content='http://www.w3.org/2002/08/xhtml/xhtml1-strict.xsd'/>",
"</i>", "</p>", "</body>", "</html>", "<head>", "<title>", "</title>",
"</head>", "<body>", "<p>", "<html>", "<b>", "<i>", "</b>", "\u2019", "\u201c", 
"\u201d", "\u2014", "\u2018", "\n", "\u2026", "\u2032", "\u2013", "\"", "\u0097"]

def unpack_file(tar, parquet):
    '''
    Extract compressed files from tarball and parquet and return as a pandas
    dataframe.

    Inputs:
        tar (string): filepath to tar file
        parquet (string): filepath to parquet file
    Output:
        df_jsons (pandas dataframe): pandas dataframe of JSON files, where
            each file is an article
    '''
    with tarfile.open(tar) as tz_file:
        parquet_file = tz_file.extractall(sys.path[-1] + '/data/proquest_files')
        parquet_file = tz_file.extractfile(parquet)
        df_jsons = pd.read_parquet(parquet_file)
        tz_file.close()
    return df_jsons

def convert_to_dict(tar, parquet, newspaper_id, url_counter = 0):
    '''
    Convert pandas dataframe of JSON's to dictionaries, containing the following
    keys.
        * 'candidate_id'
        * 'name_tokens'
        * 'announcement_date'
        * 'newspaper_id'
        * 'url'
        * 'title'
        * 'text'
        * 'date'
    The values for the last 5 keys will be assigned in this function with data
    from the article JSON. The first 3 will be initialized to None, and will
    have values assigned later when the articles are paired with a candidate.
    Since URLs do not exist for these articles, each article will be assigned a
    unique number in the URL field.

    Inputs:
        tar (string): filepath to tar file
        parquet (string): filepath to parquet file
        newspaper_id (string): Unique ID for the newspaper being analyzed
    Output:
        df_jsons (pandas dataframe): pandas dataframe of JSON files, where
            each file is an article
    '''
    df_jsons = unpack_file(tar, parquet)
    all_results = []
    for row in df_jsons.iterrows():
        url_counter += 1
        row_json = json.loads(row[1]['Data'])
        text = row_json["RECORD"]["TextInfo"]['Text']['#text']
        text_clean_i = re.sub('\u00ed', 'i', text)
        text_clean_u = re.sub('\u00fa', 'u', text_clean_i)
        text_clean = re.sub('|'.join(STRINGS_TO_REMOVE), ' ', text_clean_u)
        url = url_counter
        title = row_json["RECORD"]['Obj']['TitleAtt']['Title']
        title_clean_i = re.sub('\u00ed', 'i', title)
        title_clean_u = re.sub('\u00fa', 'u', title_clean_i)
        title_clean = re.sub('|'.join(STRINGS_TO_REMOVE), ' ', title_clean_u)
        pub_date = row_json["RECORD"]['Obj']['NumericDate']
        result_dict = {'candidate_id': None, 'name_tokens': None,
                       'announcement_date': None, 'newspaper_id': newspaper_id,
                       'url': url, 'title': title_clean.strip(), 
                       'text': text_clean.strip(),'date': pub_date}
        all_results.append(result_dict)
    return all_results
