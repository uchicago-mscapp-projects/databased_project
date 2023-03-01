'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: clean.py
Associated files: 
Primary Authors: Kathryn Link-Oberstar, Maddie Roberts
    * <Function Name> - <Function Author>

Clean JSON files of scraped articles.
'''
import unicodedata
import sys
import re
import os
import pandas as pd
import json

# Import Search Strings Function to retrieve candidate names from database
from data_retrieval import search_strings

#Set Filepath
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# The function to strip unicode charachters is adapted from a function used in 
# CAPP 121, Programming Asssignment #3
def strip_unicode(ch):
   '''
   Find all characters that are classifed as punctuation in Unicode
   (except ., !, ?) and combine them into a single string.
   '''
   return unicodedata.category(ch).startswith('P') and \
       (ch not in (".", "!", "?"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                       if strip_unicode(chr(i))])

STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "in", "is",
              "at", "it", "chicago", "mayor", "mayoral"]

STOP_WORDS_FORMAT = r'\b('+'|'.join(STOP_WORDS)+r')\b'

def clean(filepath, paper_id):
    '''
    This function takes the filepath of a JSON files containing a list of
    articles to clean. It returns an update list of articles, where three 
    additional keys have been added:
        * Clean Title: remove unicode charachters, stop words, 
    '''
    with open(sys.path[-1]+ filepath) as f:
        articles = json.load(f)
    
    for article in articles:
        article["Clean Title"] = clean_title(article)
        article["Clean Text"] = clean_text(article)
        article["Clean Strings"] = clean_sentences(article, article["Clean Text"], paper_id)
 
    return articles

def clean_title(article):
    clean_title = article['Title'].strip().lower()
    remove_words_title = re.sub(STOP_WORDS_FORMAT,' ', clean_title)
    clean_title = re.sub(r'\s+', '', remove_words_title).strip()
    return clean_title

def clean_text(article):
    clean_text = article['Text'].strip(PUNCTUATION).lower()
    remove_punct = re.sub(r'[\"\'\,\;\:\(\)\”\’\“]', '', clean_text)
    replace_end = re.sub(r'[\n?!]', '.', remove_punct)
    remove_words = re.sub(STOP_WORDS_FORMAT,'', replace_end)
    clean_text = re.sub(r'\s+', ' ', remove_words).strip()
    return clean_text

def clean_sentences(article, clean_text, paper_id):
    newpaper_db = search_strings(newspaper_id = paper_id)
    cand_name_dict = (newpaper_db.groupby('candidate_id')['name_tokens']
                        .apply(lambda x: [token.lower().strip() for token in set(x)])
                        .to_dict())
    final_sent = []
    for sent in clean_text.split("."):
        for cand_id, name_tokens in cand_name_dict.items():
            if cand_id == article['candidate_id']:
                for name in name_tokens:
                    if name in sent:
                        final_sent.append(sent)
                        break
    return final_sent

def export_clean(filename, paper_id):
    all_articles = clean(filename, paper_id)
    df = pd.DataFrame(all_articles)
    print(df)
    ## For Debugging
    print("Writing json")
    filepath = sys.path[-1] + '/data/clean_articles.json'
    with open(filepath, "w") as f:
        json.dump(all_articles, f, indent=1)