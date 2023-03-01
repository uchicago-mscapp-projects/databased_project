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
from data_retrieval import search_strings

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "in", "is",
              "at", "it", "chicago", "mayor", "mayoral", "s", "t", "u.s."]

STOP_WORDS_FORMAT = r'\b('+'|'.join(STOP_WORDS)+r')\b'

def clean(filepath, paper_id):
    '''
    This function takes the filepath of a JSON files containing a list of
    articles to clean. It returns an update list of articles, where three 
    additional keys have been added:
        * Clean Title: remove unicode charachters, stop words, 
    '''
    with open(sys.path[-1] + filepath) as f:
        articles = json.load(f)

    for article in articles:
        article["Clean Title"] = clean_title(article)
        article["Clean Text"] = clean_text(article)
        article["Clean Strings"] = clean_sentences(article, article["Clean Text"], paper_id)
    return articles

def clean_title(article):
    clean_title = article['Title'].strip().lower()
    remove_punct = re.sub(r'[^\w\s]', '', clean_title)
    remove_words_title = re.sub(STOP_WORDS_FORMAT,' ', remove_punct)
    clean_title = re.sub(r'\s+',' ', remove_words_title)
    return clean_title

def clean_text(article):
    clean_text = article['Text'].lower()
    remove_ald = re.sub(r'(ald\.|rep\.)',' ', clean_text)
    remove_punct = re.sub(r'[^\w\s.!?]+',' ', remove_ald) # remove tabs
    replace_end = re.sub(r'[\n?!]', '.', remove_punct)
    remove_words = re.sub(STOP_WORDS_FORMAT,' ', replace_end)
    clean_text = re.sub(r'\s+',' ', remove_words)
    return clean_text

def clean_sentences(article, clean_text, paper_id):
    newpaper_db = search_strings(newspaper_id = paper_id)
    cand_name_dict = (newpaper_db.groupby('candidate_id')['name_tokens']
                        .apply(lambda x: [token.lower().strip() for token in set(x)])
                        .to_dict())
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

# what to call ... papers = [("/data/crain.json", 'news_cc'), ("/data/chicago_tribune.json", 'news_ct')]
# Export Clean Articles
def export_clean(papers):
    '''
    Takes list of tuples where the tuple is the filepath to the paper's JSON 
    file of articles and the newspaper id
    For example: [("/data/crain.json", 'news_cc'), 
    ("/data/chicago_tribune.json", 'news_ct')] would return the cleaned articles
    for Crain Business journal and the Chicago Tribune.
    '''
    all_articles = []
    for paper in papers:
        filename, paper_id = paper
        all_articles += clean(filename, paper_id)
    df = pd.DataFrame(all_articles)
    print(df)
    ## For Debugging
    print("Writing json")
    filepath = sys.path[-1] + '/data/clean_articles.json'
    with open(filepath, "w") as f:
        json.dump(all_articles, f, indent=1)