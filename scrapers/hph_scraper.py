import json
import lxml.html
import requests
import pandas as pd
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings
    

def build_url(name_token, start_date):
    date_format = '2022-01-20'
    name_list = name_token.split()
    name_plus_delimited = '+'.join(name_list)
    name_plus_delimited = name_plus_delimited.replace("'", "%27")
    example_url = f'https://www.hpherald.com/search/?f=html&q=%22{name_plus_delimited}%22+mayor&d1={start_date}]&s=start_time&sd=desc&l=100&t=article&nsa=eedition'
    return None

def scrape_article(url):
    response = requests.get(url).text
    root = lxml.html.fromstring(response)
    return None

def get_article_urls(url):
    response = requests.get(url).text
    root = lxml.html.fromstring(response)
    links = root.xpath("/html/body/div[4]/div/div[6]/section[2]/div[2]/div[1]/div/div[3]/article[*]/div[1]/div[2]/div[2]/h3/a")
    
    urls = []
    for link in links:
        urls.append(link.get("href"))
    
    return urls

def next_page():
    return url

def candidate_scrape():
    return json_object

def hph_scrape():
    # get the input info
    cand_data = search_strings('news_hp')
    for row in cand_data.itertuples(index=False):
        build_url(name_token=row.name_tokens, start_date=row.announcement_date)
    
    # for each row in that df, run the candidate scraper
    # extend list of all json objects
    # figure out how you want this to be exported
    

if __name__ == "__main__":
    url = build_url()
    
    