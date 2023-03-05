'''
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBASED

File name: clean.py
Associated files: None
Author: Kathryn Link-Oberstar

Clean JSON files of scraped articles and return two JSON files with a list of
clean article dictionaries.

clean_articles.json returns a deduplicated list of dictionaries of articles used
for analysis with the following keys:
    * "candidate_id"
    * "name_tokens"
    * "announcement_date"
    * "newspaper_id"
    * "url"
    * "date"
    * "title"
    * "text"
    * "clean_title"
    * "clean_text"
    * "clean_sentences"

clean_articles_abr.json is an abridged version of clean_article.json that
is about half the size, and is easier to open and read. Article dictionaries
contain the following keys:
    * "candidate_id"
    * "name_tokens"
    * "announcement_date"
    * "newspaper_id"
    * "url"
    * "date"
    * "clean_title"
    * "clean_sentences"

Must run !python3 -m pip install nltk and nltk.download("stopwords")
'''
# !python3 -m pip install nltk
# nltk.download("stopwords")
import sys
import re
import os
import json
import pandas as pd
from nltk.corpus import stopwords

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Define and format stopwords
additional_stop_words =  ['000', 'ald.', 'alderman', 'alderwoman', 'also', 'amp',
                          'candidate', 'candidates', 'chicago', 'city',
                          'commissioner', 'congressman', 'cook', 'county', 'de',
                          'del', 'el', 'en', 'former', 'get', 'gets', 'illinois',
                          'la', 'las', 'lopez', 'los', 'mayor', 'mayoral',
                          'mayors', 'office','one', 'q', 'que', 'raymond', 'rep',
                          'rep.', 'representative', 'said', 'say', 'says', 'state',
                          'un', 'una', 'vs.', 'www']

standard_stop_words = stopwords.words('english')
standard_stop_words.extend(additional_stop_words)
STOP_WORDS = r'\b('+'|'.join(standard_stop_words)+r')\b'

# Create dictionary of candidate name tokens
clean_name_tokens = pd.read_csv(sys.path[-1] + '/data/cleaning_name_tokens.csv')
CAND_NAME_TOKENS = (clean_name_tokens.groupby('candidate_id')['name_tokens']
                    .apply(lambda x: [token.lower().strip() for token in set(x)])
                    .to_dict())

def export_clean():
    '''
    Reads article data from multiple JSON files, cleans and de-duplicates the
    data, and writes the cleaned data to two JSON files on disk, a full version
    for analysis, and an abridged file that is more easily human readable.

    Inputs:
        None

    Outputs:
        None. Writes clean_articles.json and clean_articles_abr.json
            to the data folder.
    '''
    papers = ["/data/crain.json", "/data/chicago_tribune.json",
              "/data/defender.json", "/data/hph.json","/data/ln.json",
              "/data/triibe.json"]

    all_articles = []
    for paper in papers:
        all_articles += clean(paper)

    article_df = pd.DataFrame(all_articles)
    dedupe_df = article_df.drop_duplicates(subset = ['candidate_id', 'url'],
                                keep = 'last').reset_index(drop = True)

    # Clean files for analysis
    print("Writing clean_articles json")
    filepath = sys.path[-1] + '/data/clean_articles.json'
    dedupe_df.to_json(filepath, orient='records')

    # Abridged clean file that is human readable
    print("Writing clean_articles_abridged.json")
    filepath_abr = sys.path[-1] + '/data/clean_articles_abr.json'
    dedupe_df_drop = dedupe_df.drop(['title','text','clean_text'], axis = 1)
    dedupe_df_drop.to_json(filepath_abr, orient= 'records')

def clean(filepath):
    '''
    This function takes the filepath of a JSON file containing a list of
    article dictionaries to clean. It returns an updated list of article
    dictionaries, where three additional keys have been added:
        * clean_title: title, lowercase, remove stop words, remove
            non-alphanumeric charachters
        * clean_text: text, lowercase, remove stop words, remove non-alphanumeric
            charachters except for end of sentance punctuation
        * clean_sentences:concatenated string of cleaned sentences containing
            candidate names.
    '''
    with open(sys.path[-1] + filepath) as f:
        articles = json.load(f)

    for article in articles:
        article["clean_title"] = clean_string(article,'title')
        article["clean_text"] = clean_string(article,'text')
        article["clean_sentences"] = clean_sentences(article,
                                        article["clean_text"], CAND_NAME_TOKENS)
    return articles

def clean_string(article, key):
    '''
    Cleans and normalizes a string by removing stop words, punctuation, and
        excess whitespace.

    Inputs:
        article (dict): A dictionary containing the article data
        key (str): A string indicating which key of the article dictionary
            to clean.

        Outputs:
            clean_str (str): A cleaned and normalized string.
    '''
    str_to_clean = article[key].lower()
    remove_words = re.sub(STOP_WORDS, ' ', str_to_clean)
    if key == 'text':
        remove_punct = re.sub(r'[^\w\s.!?]+', ' ', remove_words)
        replace_line_break = re.sub(r'[\n?!]', '.', remove_punct)
        stripped_str = replace_line_break
    else:
        remove_punct = re.sub(r'[^\w\s]', ' ', remove_words)
        stripped_str = remove_punct
    clean_str = re.sub(r'\s+',' ', stripped_str)
    return clean_str

def clean_sentences(article, clean_text, cand_name_dict):
    '''
    Extracts sentences from cleaned text containing candidate names and returns
        a concatenated string.

    Inputs:
        article (dict): A dictionary containing the article data
        clean_text (str): A cleaned string containing text data from the article
        cand_name_dict (dict): A dictionary mapping candidate IDs to lists of
            candidate name tokens

    Outputs:
        cleaned_sent (str): A concatenated string of cleaned sentences
            containing candidate names
    '''
    final_sent = []
    for sent in clean_text.split("."):
        sent_strip = sent.strip()
        for cand_id, name_tokens in cand_name_dict.items():
            if cand_id == article['candidate_id']:
                for name in name_tokens:
                    if name in sent_strip:
                        final_sent.append(sent_strip)
                        break
    cleaned_sent = ' '.join(final_sent)
    return cleaned_sent

if __name__ == "__main__":
    export_clean()
