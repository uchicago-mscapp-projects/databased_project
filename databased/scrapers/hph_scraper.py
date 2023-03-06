"""
Project: Analyzing News Coverage of Chicago's 2023 Mayoral Election
Team: dataBased
File Name: hph_scraper.py
Author: Abe Burton

Outputs:
    hph.json in data folder
    
Description: Scraper for Hyde Park Herald that outputs data in a json file
"""
import json
import lxml.html
import requests
import pandas as pd
import os
import sys
import time
import copy

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
    name_plus_delimited = "+".join(name_list)
    name_plus_delimited = name_plus_delimited.replace("'", "%27")
    url = f"https://www.hpherald.com/search/?f=html&q=%22{name_plus_delimited}%22+mayor&d1={start_date}&s=start_time&sd=desc&l=100&t=article&nsa=eedition"

    return url


def get_article_urls(url):
    """
    Get all the article links on a page of results

    Inputs:
        url (str): The url of the search results page

    Outputs:
        urls (lst of strings): List of article urls
    """
    try:
        response = requests.get(url).text
        root = lxml.html.fromstring(response)
        links = root.xpath(
            "/html/body/div[4]/div/div[6]/section[2]/div[2]/div[1]/div/div[3]/article[*]/div[1]/div[2]/div[2]/h3/a"
        )
    except:
        print(f"Couldn't get list of articles for {url}")
        return False

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
    try:
        url = "https://www.hpherald.com/" + url
        print(f"Fetching {url}")
        response = requests.get(url).text
        root = lxml.html.fromstring(response)
        date = root.xpath("//time[1]")[0].text_content()
        date = str(pd.to_datetime(date)).split()[0]
        title = root.xpath("//article/div[3]/header/h1/span")[0].text_content()
        paragraphs = root.cssselect("p")
        text = ""
        for paragraph in paragraphs:
            if paragraph.text_content() == "{{description}}":
                break
            text += paragraph.text_content()
    except:
        print(f"Couldnt get article info for {url}")
        return False

    return url, title, text, date


def hph_scrape():
    """
    Runs the scraper to get all article info from HPH

    Outputs:
        hph.json: json file with a list of json objects of article data
    """
    # get the input info
    cand_data = search_strings("news_hp")
    cand_data = cand_data.to_dict("index")

    # search each token and scrape all article results for them
    json_list = []
    for _, val in cand_data.items():
        url = build_url(
            name_token=val["name_tokens"], start_date=val["announcement_date"]
        )
        article_links = get_article_urls(url)

        if article_links:
            for link in article_links:
                article_dict = copy.deepcopy(val)
                article_data = scrape_article(link)
                if article_data:
                    url, title, text, date = article_data
                    article_dict["url"] = url
                    article_dict["title"] = title
                    article_dict["text"] = text
                    article_dict["date"] = date
                    json_list.append(article_dict)
                    time.sleep(0.1)

    print("Writing hph.json")
    filepath = sys.path[-1] + "/data/hph.json"
    with open(filepath, "w") as f:
        json.dump(json_list, f, indent=1)


if __name__ == "__main__":
    hph_scrape()
