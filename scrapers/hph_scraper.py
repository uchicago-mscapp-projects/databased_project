"""
This is the Hyde Park Herald Scraper Module

Outputs:
    List of json objects at (location)
"""
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
    """
    Takes a name token and a start date and returns a url that conducts
    an advanced search of articles on the HPH website
    
    Inputs:
        name_token (str): The name to be used in the candidate search
        start_date (str): The date to start searching for articles
        
    Outputs:
        url (txt): The url string to search
    """
    start_date = str(pd.to_datetime(start_date)).split()[0]
    name_list = name_token.split()
    name_plus_delimited = '+'.join(name_list)
    name_plus_delimited = name_plus_delimited.replace("'", "%27")
    url = f'https://www.hpherald.com/search/?f=html&q=%22{name_plus_delimited}%22+mayor&d1={start_date}&s=start_time&sd=desc&l=100&t=article&nsa=eedition'
    
    return url


def get_article_urls(url):
    """
    Get all the article links on a page of results
    
    Inputs:
        url (str): The url of the search results page
        
    Outputs:
        urls (lst of strings): List of article urls
    """
    response = requests.get(url).text
    root = lxml.html.fromstring(response)
    links = root.xpath("/html/body/div[4]/div/div[6]/section[2]/div[2]/div[1]/div/div[3]/article[*]/div[1]/div[2]/div[2]/h3/a")
    
    urls = []
    for link in links:
        urls.append(link.get("href"))
    
    return urls


def scrape_article(url):
    """
    Scrape the necessary info from the article
    
    Inputs:
        url (str): article url to be scraped
    
    Outputs:
        article_dataset_row (json): a json object with article dataset info
    """
    url = 'https://www.hpherald.com/' + url
    response = requests.get(url).text
    root = lxml.html.fromstring(response)
    date = root.xpath('//time[1]')[0].text_content()
    date = str(pd.to_datetime(date)).split()[0]
    # do we really need what the search field was?
    title = root.xpath('//article/div[3]/header/h1/span').text_content()
    # look at how to make this more relative so it breaks less!
    text = root.xpath('//article//p').text_content()
    # don't see any tags
    site_id = 'news_hp'
    cand_id = '' # figure out passing this through the functions
    
    # create json object with these things and return it
    # TODO figure out where this fits in. 
    print("Writing defender.json")
    with open("defender.json", "w") as f:
        json.dump(pages, f, indent=1)
        
    # TODO lee - or is writing to an article dictionary each time and then turning putting all
    # dictionary items in a list and then making that json object
    return article_dataset_row


def hph_scrape():
    """
    Runs the scraper to get all article info from HPH
    
    Outputs:
        TBD
    """
    # get the input info
    cand_data = search_strings('news_hp')
    for row in cand_data.itertuples(index=False):
        url = build_url(name_token=row.name_tokens, start_date=row.announcement_date)
        article_links = get_article_urls(url)
        
        json_list = []
        for link in article_links:
            json_list.append(scrape_article(link))
            
        # TODO where do I want to export this? Is this really the format?
        # export one json file that contains all article objects to the data folder
        # TODO send filepath code to lee-or so he can write to data directory
    

if __name__ == "__main__":
    hph_scrape()
    
    