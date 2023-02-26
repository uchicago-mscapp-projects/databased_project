'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: export.py
Associated files: process_articles.py, select_articles.py
Primary Author: Kathryn Link-Oberstar
Addiditional Authors: None

Description: Convert xml files from Proquest Dataset into a list of JSON files 
to export. Proquest allows users to create a dataset of articles by selecting a 
publication, and applying fitler parameters. This module takes a Proquest 
dataset (a folder of xml files - one for each newssource sepcified below) 
from April 11, 2022 (the date of the first mayoral candidate's annoucement) 
to February 28, 2023 (election day) with the keyword "mayor". This module 
converts each file to a JSON, and appends the JSON to a list. The final list 
is converted to a pandas dataframe, then compressed with parquet and tarball 
to stay within the Proquest 15MB weekly download limit. 
This files runs directly in ProQuest virtual environment. This function was run 
3 times for:
    * Chicago Tribune (Online) 2022
    * Chicago Tribune (Online) 2023
    * Crain Business Journal
'''
import xmltodict
import pyarrow
import os
import json
import pandas as pd


# Replace FILES_TO_EXPORT, PARQ_FILE_PATH and TZ_FILE_PATH with correct file paths
FILES_TO_EXPORT = ""
PARQ_FILE_PATH = ""
TZ_FILE_PATH = ""

# For Chicago Tribune 2022
#FILES_TO_EXPORT = "data/Chicago_Tribune_-_Mayor_-_2022"
#PARQ_FILE_PATH = "data/chicago_tribune_2022.parquet"
#TZ_FILE_PATH = "data/chicago_tribune_2022.tar.gz"

# For Chicago Tribune 2023
#FILES_TO_EXPORT = "data/Chicago_Tribune_-_Mayor_-_2023"
#PARQ_FILE_PATH = "data/chicago_tribune_2023.parquet"
#TZ_FILE_PATH = "data/chicago_tribune_2023.tar.gz"

# For Crain Business Journal
#FILES_TO_EXPORT = "data/Crain_-_Mayor"
#PARQ_FILE_PATH = "data/crain.parquet"
#TZ_FILE_PATH = "data/crain.tar.gz"

# Convert folder of xml files to list of JSON files
file_list = os.listdir(FILES_TO_EXPORT)
file_list = [file for file in file_list if file.endswith("xml")]

list_of_file_data = []

for file in file_list:
    file_path = os.path.join(FILES_TO_EXPORT, file)
    with open(file_path, "r") as f:
        file_as_xml = f.read()
        file_as_dict = xmltodict.parse(file_as_xml)
        list_of_file_data.append(json.dumps(file_as_dict))

# Write Dataframe to parquet and then tarball to compress file size for export
df = pd.DataFrame(list_of_file_data)
df.columns = ["Data"]
df.to_parquet(PARQ_FILE_PATH)

# Compress with tarball
# Chicago Tribune 2022
#!tar -czvf data/chicago_tribune_2022.tar.gz data/chicago_tribune_2022.parquet

# Chicago Tribune 2023
#!tar -czvf data/chicago_tribune_2023.tar.gz data/chicago_tribune_2023.parquet

# Crain Business
!tar -czvf data/crain.tar.gz data/crain.parquet

# Calculate final file size (to stay within Proquest file size limit)
file_size = os.path.getsize(TZ_FILE_PATH)
print(f"Size of file: {file_size/1000000} MB")
