"""
Project: CAPP 122 DataBased Project
File name: scrape_lawndale.py

Scrapes data from lawndale news pages pages.

Methods:
    * scrape_ln - scrapes data for mayoral candidates.
    * scrape_all_pages - scrapes data for passed candidate tokens.
    * get_first_search_page - finds first page of search results for passed candidate tokens.
    * get_article_urls - finds all park URLs on page.
    * get_next_page - finds URL to next page of article lists.
    * scrape_article - scrapes article page.
    * date_convert - converts string to a datetime object.
    * make_request - make a request to 'url' and return the raw response.

@Author: Madeleine Roberts
@Date: Feb 26, 2023
"""

import sys
import json
import lxml.html
from datetime import datetime
import os
import time
import requests

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings

ELECTION_DAY = datetime(2023, 2, 28)

def scrape_ln():
    """
    Scrapes all articles from lawndale news that are associated with the candidates 
    and candidate tokens in the database.

    Returns: 
        * A json file that contains all scraped articles for all candidates.
    """
    # Retrieve all candidate information from database
    cand_data = search_strings('news_ln')
    cand_data = cand_data.to_dict('index')

    json_list = []

    # Run scraper for each unique token and output to json file
    for _, val in cand_data.items():
        announcement_date = date_convert(val['announcement_date'], 1)

        article_list_for_token = scrape_all_pages(val['candidate_id'], val['name_tokens'], announcement_date)
        json_list += article_list_for_token
        
    print("Writing ln.json")
    filepath = sys.path[-1] + '/data/ln.json'
    with open(filepath, "w") as f:
        json.dump(json_list, f, indent=1)

def scrape_all_pages(candid, name_tokens, announcement_date):
    """
    This function takes a candidate id, the name tokens to search for, and their
    announcement date to scrape all articles associated with these tokens.

    Parameters:
        * candidate_id: candidate id in database
        * name_tokens:  specified search string
        * announcement_date: date of candidate announcement

    Returns:
        A list of scraped articles
    """

    # Retreive correct search url
    current_url = get_first_search_page(name_tokens) 
    list_of_article_urls = []
    list_of_scraped_pages = []

    while(current_url): 
        # Scrape pages
        print(current_url)
        article_urls = get_article_urls(current_url, announcement_date)
        list_of_article_urls = list_of_article_urls + article_urls
        current_url = get_next_page(current_url)


    # Scrape all pages
    for page_url in list_of_article_urls:
        #print(page_url)
        page_dict = scrape_article(page_url, candid, name_tokens, announcement_date)
        list_of_scraped_pages.append(page_dict)

    return list_of_scraped_pages
    
def get_first_search_page(full_name):
    """
    Retrieves the first page of search results for a specific name token.

    Parameters:
        * full_name (string): name tokens to include in the search

    Returns:
        URL to the first search page of the given tokens
    """
    
    split_name = full_name.split()
    search_name = "%22" + "+".join(split_name) + "%22+mayor"
    url = f"http://www.lawndalenews.com/?s={search_name}&x=0&y=0"
    return url

def get_article_urls(url, announcement_date):
    """
    This function takes a URL to a page of lawndale news and returns a
    list of URLs to each park on that page.

    Parameters:
        * url:  a URL to a page of parks

    Returns:
        A list of URLs to each park on the page.
    """

    # Temp link
    page = make_request(url)
    root = lxml.html.fromstring(page.text)

    urls = []
    rows = root.cssselect("#main #container #content")
    elements = rows[0].cssselect("div.gridrow")

    
    # Current structure of page is 3 containers, each which has at most two articles
    if len(elements) > 5:
        raise Exception ("Page structure has changed: more than 5 containers for articles")
    
    # Scape all website links in table
    for element in elements:
        articles = element.cssselect("div h2")
        article_dates = element.cssselect("div div .meta-date")

        if len(articles) > 2:
            raise Exception ("Page structure has changed: more than 2 articles in container")

        for (article, date) in zip(articles, article_dates):
            
            # Check the date is not prior to announcement
            parsed_date = date_convert(date.text_content(), 0)
            if parsed_date < announcement_date or parsed_date > ELECTION_DAY:
                # Article was written prior to announcement
                continue

            article_url = article[0].cssselect("a")[0].get("href")

            urls.append(article_url)
       
    return urls

def get_next_page(url):
    """
    This function takes a URL to a page of newpaper articles and returns a
    URL to the next page of articles if one exists.

    Parameters:
        * url (string): url to page of newpaper articles
    
    Returns:
        A string that contains the next page of newpaper articles. If no next page exists, this function returns None.
    """
    
    page = make_request(url)
    root = lxml.html.fromstring(page.text)

    # Check no search results
    if root.cssselect("body")[0].get("class") == 'search search-no-results custom-background':
        return None

    rows = root.cssselect("#main #container #content")
    page_nav = rows[0].cssselect("div")[-1]
    last_link = page_nav.cssselect("a")[-1]
    

    if last_link.get("class") == "current":
        # this is the last page
        return None
    elif last_link.text_content() == "Next »":
        link_to_next_page = last_link.get("href")
    
        return link_to_next_page
    else:
        # single page of results
        return None


def scrape_article(url, cand_id, name_tokens, announcement_date):
    """
    This function takes a URL to a Lawndale newspaper article page and its repesective 
    database tokens and returns a dictonary with database tokens (candidate_id,
    name_tokens, announcement_date, and newspaper_id), url to article, article title,
    article text, and article date.

    Parameters:
        * url (string):  a URL to a newspaper aticle page
        * cand_id (string): candidate id in database
        * name_tokens (string): specified search string
        * announcement_date (datetime object): date of candidate announcemnt

    Returns:
        A dictionary with the following keys:
            * candidate_id: candidate id in database
            * name_tokens:  specified search string
            * announcement_date: date of candidate announcement
            * newspaper_id: newspaper id in database
            * url:          the URL of the article page
            * title:        the title of article
            * text:         the text content of the article
            * date:         the description of the park
    """
    page = make_request(url)
    root = lxml.html.fromstring(page.text)

    article = root.cssselect("#main #container #content div") 

    # Get article title
    title = article[0].cssselect(".entry-title")[0].text_content()

    # Get date, and convert to date format 
    # Date structure: string "on April 2, 2022"
    date = article[0].cssselect(".meta-date")[0].text_content()

    if date[:3] == "on ":
        date = date[3:]
    
    parsed_date = date_convert(date, 0)

    # Get article text
    # Note: this includes the author and editor; this should be removed in the cleaning 
    full_text = article[0].cssselect("div.entry-content")[0].text_content()

    full_article = {
        'candidate_id' : cand_id,
        'name_tokens' : name_tokens,
        'announcement_date' : announcement_date.strftime("%d-%b-%y"),
        'newspaper_id' : "news_ln",
        'url' : url,
        'title' : title,
        'text' : full_text,
        'date' : parsed_date.strftime("%d-%b-%y")
    }

    return full_article

def date_convert(date, flag):
    """
    Converts string to a datetime object

    Parameters:
        * date (string): the date to be converted
        * flag (int): indicates the structure of date string

    Return:
        A datetime object corrisponding to the string
    """
    try:
        if flag:
            parsed_date = datetime.strptime(date, '%d-%b-%y')
        else:
            parsed_date = datetime.strptime(date, '%B %d, %Y')
        return parsed_date
    except TypeError:
        raise("Error in date parsing: Format has changed. Type Error")
    except ValueError:
        raise("Error in date parsing: Format has changed. Value Error")
    except: 
        raise("Error in date parsing: Format has changed.")

def make_request(url):
    """
    Make a request to 'url' and return the raw response.

    Parameters:
        * url (string): a URL to a newspaper aticle page
    
    Returns:
        Raw response for url
    """
    time.sleep(0.1)
    resp = requests.get(url)
    return resp

if __name__ == "__main__":
    scrape_ln()
    
