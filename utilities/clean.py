'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: clean.py
Associated files: None
Primary Authors: Kathryn Link-Oberstar

Clean JSON files of scraped articles.

'''

'''
Function Call
papers = ["/data/crain.json", "/data/chicago_tribune.json", "/data/defender.json", 
"/data/hph.json","/data/ln.json", "/data/triibe.json"]

clean.export_clean(papers)
'''
#!python3 -m pip install nltk

import nltk
import sys
import re
import os
import pandas as pd
import json
from nltk.corpus import stopwords
from data_retrieval import search_strings

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# nltk.download("stopwords")
add_stop_words = ['mayor','representative','alderman', 'chicago', 'il'
                                           'alderwoman', 'mayors', 'mayoral',
                                           'congressman', 'amp', 'illinois', 
                                           'said', 'would', 'city', 'also', 
                                           'former','county', 'state', 
                                           'commissioner', 'candidate', 
                                           'candidates', 'raymond', 'lopez', 
                                           'one', 'office', 'say', 'says', 'cook'
                                           ,'de', 'get', 'que', 'la', 'el', 'en', 
                                           'get', 'q', 'los', 'las', 'del', 'una', 
                                           '000', 'un', 'gets','www','com', 'rep']

stop_words = stopwords.words('english')
stop_words.extend(add_stop_words)
print(stop_words)
stop_words_format = r'\b('+'|'.join(stop_words)+r')\b'
print(stop_words_format)

def clean(filepath):
    '''
    This function takes the filepath of a JSON files containing a list of
    articles to clean. It returns an update list of articles, where three 
    additional keys have been added:
        * Clean Title: remove unicode charachters, stop words, 
    '''
    with open(sys.path[-1] + filepath) as f:
        articles = json.load(f)

    clean_name_tokens = pd.read_csv(sys.path[-1] + '/data/cleaning_name_tokens.csv')
    cand_name_dict = (clean_name_tokens.groupby('candidate_id')['name_tokens']
                        .apply(lambda x: [token.lower().strip() for token in set(x)])
                        .to_dict())

    for article in articles:
        article["clean_title"] = clean_title(article)
        article["clean_text"] = clean_text(article)
        article["clean_sentences"] = clean_sentences(article, article["clean_text"], cand_name_dict)
    return articles

def clean_title(article):
    clean_title = article['title'].strip().lower()
    remove_words_title = re.sub(stop_words_format,' ', clean_title)
    remove_punct = re.sub(r'[^\w\s]', '', remove_words_title)
    clean_title = re.sub(r'\s+',' ', remove_punct)
    return clean_title

def clean_text(article):
    clean_text = article['text'].lower()
    remove_words = re.sub(stop_words_format,' ', clean_text)
    remove_ald = re.sub(r'(ald\.|rep\.|vs\.)',' ', remove_words)
    remove_punct = re.sub(r'[^\w\s.!?]+',' ', remove_ald)
    replace_end = re.sub(r'[\n?!]', '.', remove_punct)
    clean_text = re.sub(r'\s+',' ', replace_end)
    return clean_text

def clean_sentences(article, clean_text, cand_name_dict):
    
    final_sent = []
    for sent in clean_text.split("."):
        sent_strip = sent.strip()
        for cand_id, name_tokens in cand_name_dict.items():
            if cand_id == article['candidate_id']:
                for name in name_tokens:
                    if name in sent_strip:
                        final_sent.append(sent_strip)
                        break
    return ' '.join(final_sent)

def export_clean(papers):
    '''
    Takes list of tuples where the tuple is the filepath to the paper's JSON 
    file of articles and the newspaper id.
    '''
    all_articles = []
    for paper in papers:
        all_articles += clean(paper)
    
    df = pd.DataFrame(all_articles)
    dedupe_df = df.drop_duplicates(subset = ['candidate_id', 'url'], 
                                keep = 'last').reset_index(drop = True)
    print(dedupe_df)
    '''
    print("Writing clean_articles json")
    filepath = sys.path[-1] + '/data/clean_articles.json'
    dedupe_df.to_json(filepath, orient='records')
    '''
    print("Writing clean_articles_ abridged.json")
    filepath_abr = sys.path[-1] + '/data/clean_articles_abr.json'
    dedupe_df_drop = dedupe_df.drop(['title','text','clean_text'], axis = 1)
    dedupe_df_drop.to_json(filepath_abr, orient= 'records')