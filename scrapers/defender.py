"""
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBased
File Name: defender.py
Author: Lee-Or Bentovim

Outputs:
    defender.json in data folder

Description:
    This module is meant to take a search string and search it on the Chicago Defender
    website, and then scrapes associated URL's, outputting them into a json file called
    defender.json

Some of the original structure of this file comes from Lee-Or's PA2 work
"""

import sys
import os
import json
import lxml.html
import pandas as pd
from utils import make_request
from datetime import datetime

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utilities.data_retrieval import search_strings

# We are stopping our search at Feb 27, 2023
END_DATE = datetime(2023,2,27)

def scrape_page(article_dict, url):
    """
    This function takes a URL to a page and returns a dictionary with important
    information from an article

    Inputs:
        article_dict (dict): a dictionary pre-filled with some key-value pairs
        url (string):  a URL to a chicago defender page

    Returns:
        A dictionary with the following keys:
            candidate_id:       the id associated with the candidate
            name_tokens:        the name token associated with the search
            announcment_date:   the date the associated candidate declared
            newspaper_id:       the id associated with the newspaper
            url:                the URL of the webpage
            title:              the title of the webpage
            text:               the text of the webpage
            date:          the date the article was published
    """

    html = make_request(url).text
    root = parse_html(html)

    article_dict['url'] = url

    article_dict['title'] = root.xpath("//h1")[0].text_content()

    body = root.xpath("//p")

    doc_text = ''
    for row in body[2:-3]:
        doc_text += row.text_content()
    
    article_dict['text'] = doc_text
    date = root.xpath("//time")[0].text
    date = str(pd.to_datetime(date)).split()[0]
    article_dict['date'] = date

    return article_dict

def parse_html(html):
    """
    Parse HTML and return the root node.
    """
    return lxml.html.fromstring(html)

def get_news_urls(search_string, stop_date, current_page = 1,
                    url = "https://chicagodefender.com/page/"):
    """
    This function takes a URL to a page of articles and returns a list of URLs
    to each park on that page so long as they are later than the stop date

    Parameters:
        search_string (str):  the string to add to create the search
        stop_date (datetime): the date the candidate in search_string announced
        current_page (int): The page number for the search
        url (string): The url to search the website

    Returns:
        A list of URLs to each website on the page.
    """

    # The string needs to be "mayor + associated_name", otherwise will fix here
    search = url + str(current_page) + '/?s=' + search_string
    urls = []

    html = make_request(search).text
    root = parse_html(html)

    links = root.xpath("//main/div[3]//a")

    # We will access the dates with getnext
    dates = root.xpath("//main/div[3]//h3")
    date_list = []

    # Turns each date into a datetime object
    for item in dates:
        day = item.getnext().text
        date_list.append(pd.to_datetime(day))

    # Looping through the links on a page
    for i, link in enumerate(links):

        # Must have same number of links and dates
        if len(links) != len(dates):
            raise Exception("Dates and Links don't match")

        # Stopping Condition: Date is before candidate filed 
        # or after end of tracking period
        stop_date = pd.to_datetime(stop_date)
        if date_list[i] < stop_date:
            return urls, False
        
        # If the date is before our end date, add info
        if date_list[i] < END_DATE:
            full_url = link.get("href")
            urls.append(full_url)

    return urls, True

def check_next_page_exists(search_string, current_page, url = "https://chicagodefender.com/page/"):
    """
    This function takes a URL to a page of search results and returns the
    length of nav_list, which will be zero if on last page, and greater otherwise

    Inputs:
        search_string (str):  the string to add to create the search
        current_page (int): The page number for the search
        url (string): The url to search the website

    Outputs:
        Len(nav_list) (int): len of the nav_list, a list of page buttons objects
    """

    search = url + str(current_page) + '/?s=' + search_string + '"'

    html = make_request(search).text
    root = parse_html(html)

    # nav_list is the list of button objects, length = 0 if page does not exist
    nav_list = root.xpath("//main//li")

    return len(nav_list)

def crawl(current_page = 1, url="https://chicagodefender.com/page/"):
    """
    This function starts at the base URL for the Chicago Defender website and
    crawls through each page of the search, scraping each article before
    the stop date and saving output to a file named "defender.json".

    Inputs:
        current_page (int): The page number for the search, initially 1
        url (string): The url to search the website

    Outputs:
        None: This function will write a list of dictionaries to a json file called
        defender.json
    """

    df = search_strings(newspaper_id = 'news_cd')

    # Turns the df into a dictionary with key: index, value: dictionary of each row
    df_dicts = df.to_dict('index')

    pages = []

    # Run one while loop for each search term
    for article_dict in df_dicts.values():

        # Allows us to ensure that we start each while loop at the first page requested
        search_page = current_page

        # Will continue in loop until we pass stop date or pass last page of search
        while True:

            search_field = '"' + str(article_dict['name_tokens']) + '"+mayor'
            pages_to_add, status = get_news_urls(search_field,
                        article_dict['announcement_date'], search_page, url)

            for article in pages_to_add:
                pages.append(scrape_page(article_dict, article))

            cont = check_next_page_exists(search_field, search_page + 1, url)

            # If either we've crossed date limit or there are no more pages
            if not (cont and status):
                break

            search_page += 1

    print("Writing defender.json")
    filepath = sys.path[-1] + '/data/defender.json'
    with open(filepath, "w") as f:
        json.dump(pages, f, indent=1)
