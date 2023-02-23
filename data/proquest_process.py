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
# TO DO
# unzip tarball
# unpack parquet
# Run though JSONS looking for cand name strings and append to new list
# check the outputs?
import pyarrow
import re
import tarfile
import json
import pandas as pd

#as list of strings to file path
proquest_files = [('chicago_tribune_2022.tar', 'data/chicago_tribune_2022.parquet')]

# name tokens, call from db

#def search_files():

def unpack_files(proquest_files, name_token):
    all_results = []
    for tar, parquet in proquest_files:
        tz_file = tarfile.open(tar)
        parquet_file = tz_file.extractall("./")
        parquet_file = tz_file.extractfile(parquet)
        df_jsons = pd.read_parquet(parquet_file)
        for row in df_jsons.iterrows():
            #print("row", type(row[1]['Data']))
            row_json = json.loads(row[1]['Data'])
            #print("row_json", row_json["RECORD"])
            website_title = row_json["RECORD"]["DFS"]['PubFrosting']['Title']
            s = 'abc-xyz-123-789-ABC-XYZ'
            print(re.sub('\d+', '', s))
            text = row_json["RECORD"]["TextInfo"]['Text']['#text']
            url = None
            seach_field = f"'{name_token}' mayor"
            title = row_json["RECORD"]['Obj']['TitleAtt']['Title']
            pub_date = row_json["RECORD"]['Obj']['NumericDate']
            tags = None
            site_ID = 999
            cand_ID = 999
            results = (website_title, url, seach_field, title, text, name_token, pub_date, tags, site_ID, cand_ID)
            tz_file.close()
    all_results.append(results)
unpack_files(proquest_files, 'chuy garcia')

#Website Title (string)
#URL (string)
#Seach Field
#Title (string)
#Text (string)
#Associated Candidate (string)
#Publication Date (date)
#Tags (string)
#Site ID - foreign key
#Cand ID - foreign key
