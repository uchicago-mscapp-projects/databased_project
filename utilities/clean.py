'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: clean.py
Associated files: None
Primary Authors: Kathryn Link-Oberstar

Clean JSON files of scraped articles.
'''
import csv
import sys
import re
import os
import pandas as pd
import json

from data_retrieval import search_strings

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

STOP_WORDS = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 
               'there', 'about', 'once', 'during', 'out', 'very', 'having', 
               'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 
               'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 
               'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 
               'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 
               'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 
               'himself', 'this', 'down', 'should', 'our', 'their', 'while', 
               'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 
               'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 
               'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 
               'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 
               'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 
               'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 
               'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 
               'it', 'how', 'further', 'was', 'here', 'than', 'chicago', 'mayor', 
               'mayoral', 'we\'ve', 'we\'re', 'it\'s', 'he\s', 'she\'s']

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
        article["clean_title"] = clean_title(article)
        article["clean_text"] = clean_text(article)
        article["clean_sentences"] = clean_sentences(article, article["clean_text"], paper_id)
    return articles

def clean_title(article):
    clean_title = article['title'].strip().lower()
    remove_words_title = re.sub(STOP_WORDS_FORMAT,' ', clean_title)
    remove_punct = re.sub(r'[^\w\s]', '', remove_words_title)
    clean_title = re.sub(r'\s+',' ', remove_punct)
    return clean_title

def clean_text(article):
    clean_text = article['text'].lower()
    remove_words = re.sub(STOP_WORDS_FORMAT,' ', clean_text)
    remove_ald = re.sub(r'(ald\.|rep\.)',' ', remove_words)
    remove_punct = re.sub(r'[^\w\s.!?]+',' ', remove_ald) # remove tabs
    replace_end = re.sub(r'[\n?!]', '.', remove_punct)
    clean_text = re.sub(r'\s+',' ', replace_end)
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

papers = [("/data/crain.json", 'news_cc'), ("/data/chicago_tribune.json", 'news_ct'), 
          ("/data/defender.json", 'news_cd'), ("/data/hph.json", 'news_hp'), 
          ("/data/ln.json", 'news_ln'), ("/data/triibe.json", 'news_tt')]

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
    dedupe_df = df.drop_duplicates(subset = ['candidate_id', 'url'], 
                                keep = 'last').reset_index(drop = True)
    print(dedupe_df)
    print("Writing CSV")
    filepath = sys.path[-1] + '/data/clean_articles.csv'
    dedupe_df.to_csv(filepath, index=False)

    """
    print("Writing CSV")
    filepath = sys.path[-1] + '/data/clean_articles.csv'
    keys = ["candidate_id", "name_tokens", "announcement_date", "newspaper_id", 
            "url", "date", "title", "text", "clean_title", "clean_text", 
            "clean_sentences"]
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for article in all_articles:
            writer.writerow(article)
    """

    # For Debugging
    print("Writing json")
    filepath = sys.path[-1] + '/data/clean_articles.json'
    df.to_json(filepath, orient='records')