'''
Project: Chicago Mayor Election News Coverage

File name: proquest_export.py
Associated files: 
Primary Author: Kathryn Link-Oberstar
Addiditional Authors: None

Convert xml files from Proquest Database into a list of JSON files to export
'''
import xmltodict
import pyarrow
import os
import json
import pandas as pd

# Replace FILES_TO_EXPORT and PARQ_FILE_PATH with correct file paths

# For Chicago Tribune 2022
FILES_TO_EXPORT = "data/Chicago_Tribune_Mayor_Apr22_to_Nov22"
PARQ_FILE_PATH = "data/chicago_tribune_2022.parquet"

# For Chicago Tribune 2023
#FILES_TO_EXPORT = "data/Chicago_Tribune_-_Mayor_2023"
#PARQ_FILE_PATH = "data/chicago_tribune_2023.parquet"

# For Crain Business Journal
#FILES_TO_EXPORT = "data/Crain_Mayor_"
#PARQ_FILE_PATH = "data/crain.parquet"

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

# Write Dataframe to parquet file to compress file size for export
df = pd.DataFrame(list_of_file_data)
df.columns = ["Data"]
df.to_parquet(PARQ_FILE_PATH)

! tar -czvf data/chicago_tribune_2022.tar.gz data/chicago_tribune_2022.parquet

# Calculate the final file size (to stay within Proquest file size limit)
parq_size = os.path.getsize(data/chicago_tribune_2022.tar.gz)
print(f"Size of file: {parq_size/1000000} MB")


