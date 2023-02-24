import json
import lxml.html
import requests
import pandas as pd

def build_url():
    example_url = 'https://www.hpherald.com/search/?f=html&q=%22Lori+Lightfoot%22+mayor&d1=2022-01-20&d2=2023-01-20&s=start_time&sd=desc&l=100&t=article&nsa=eedition'
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

def hph_scraper():
    # get the input info
    # for each row in that df, run the candidate scraper
    # extend list of all json objects
    # figure out how you want this to be exported
    


if __name__ == "__main__":
    url = build_url()
    
    