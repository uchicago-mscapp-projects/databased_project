"""
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBased
File Name: triibe.py
Author: Lee-Or Bentovim

Outputs:
    triibe.json in data folder

Description:
    This module is meant to take a search string and search it on the Triibe website,
    and then scrapes associated URL's, outputting them into a json file called
    triibe.json

Some of the original structure of this file comes from Lee-Or's PA2 work
"""

import sys
import os
import json
import lxml.html
import pandas as pd
from datetime import datetime
from .utils import make_request
import copy

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

    # Some articles don't have a date. Reject them
    try:
        date = root.xpath("//time")[0].text

    except IndexError:
        print("Raising exception")
        return article_dict, False

    date = pd.to_datetime(date)

    # Checking if the article is from before candidate announced
    if date < pd.to_datetime(article_dict['announcement_date']) or date > END_DATE:
        return article_dict, False

    article_dict['date'] = date.date()

    article_dict['title'] = root.xpath("//header//h1")[0].text_content()

    body = root.xpath("//section[*]//p")

    doc_text = ''
    for row in body[1:-4]:
        doc_text += row.text_content()

    article_dict['text'] = doc_text

    # Turns announcement_date into a string for JSON
    article_dict['date'] = str(article_dict['date'])

    return article_dict, True

def parse_html(html):
    """
    Parse HTML and return the root node.
    """
    return lxml.html.fromstring(html)

def get_news_urls(search_string, url = "https://thetriibe.com/"):
    """
    This function takes a URL to a page of articles and returns a list of URLs
    to each park on that page so long as they are later than the stop date

    Parameters:
        search_string (str):  the string to add to create the search
        url (string): The url to search the website

    Returns:
        A list of URLs to each article on the page.
    """

    search = url + "?s=" + search_string

    urls = []

    html = make_request(search).text
    root = parse_html(html)

    links = root.xpath("//h2//a")

    # Looping through the links on a page
    for link in links:
        full_url = link.get("href")
        urls.append(full_url)

    return urls

def triibe_scrape(url="https://thetriibe.com/"):
    """
    This function starts at the base URL for the Chicago Defender website and
    crawls through each page of the search, scraping each article before
    the stop date and saving output to a file named "defender.json".

    This function was edited from Lee-Or's CAPP122 PA2 file

    Inputs:
        url (string): The url to search the website

    Outputs:
        None: This function will write a list of dictionaries to a json file called
        triibe.json
    """

    df = search_strings(newspaper_id = 'news_tt')

    # Turns the df into a dictionary with key: index, value: dictionary of each row
    df_dicts = df.to_dict('index')

    pages = []

    # Run one while loop for each search term
    for article_dict in df_dicts.values():

        search_field = '"' + str(article_dict['name_tokens']) + '"+mayor'
        pages_to_add = get_news_urls(search_field, url)

        for article in pages_to_add:
            page, status = scrape_page(copy.deepcopy(article_dict), article)

            # Search is not in order, must search all, only add ones before date
            if status:
                pages.append(page)

    print("Writing triibe.json")
    filepath = sys.path[-1] + '/data/triibe.json'
    with open(filepath, "w") as f:
        json.dump(pages, f, indent=1)

if __name__ == "__main__":
    triibe_scrape()
        
