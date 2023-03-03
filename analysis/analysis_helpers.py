
"""
Project: CAPP 122 DataBased Project
File name: analysis_helpers.py

General helper functions for the data analysis.

@Author: Madeleine Roberts
@Date: Mar 2, 2023
"""
# python3 -m pip install nltk
# nltk.download("stopwords")
import nltk
import json
import os
import sys
from nltk.corpus import stopwords

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings

def single_text_str(df, text_to_inspect):
    """
    Concatenates all text values in the given DataFrame column into a single string.

    Parameters:
        * df (pandas.DataFrame): The DataFrame containing the text data to concatenate.
        * text_to_inspect (str): The name of the column containing the text data to concatenate.

    Returns:
        A single string that is the concatenation of all text values in the specified column.
    """
    full_text = ""
    for __, row in df.iterrows():
        full_text += row[text_to_inspect]
        full_text += " "
    
    return full_text

def write_to_json(file_name, data_to_convert):
    """
    Writes the given dictionary of sentiment data to a JSON file with the given file name.

    Parameters:
        * file_name (str): The name of the JSON file to write to
        * data_to_convert (dict): The dictionary of  data to write to the JSON file.
    """
    print("Writing to json")
    filepath = sys.path[-1] + '/data/' + file_name

    with open(filepath, "w") as f:
        json.dump(data_to_convert, f, indent=1)