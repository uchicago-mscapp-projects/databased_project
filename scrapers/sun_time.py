'https://chicago.suntimes.com/news/2023/2/24/23610899/chicago-mayoral-election-campaign-lightfoot-vallas-johnson-garcia-strategy-runoff'

import sys
import json
import lxml.html
import pandas as pd
from datetime import datetime
from utils import make_s_request

ARTICLE_DICT = {
    "title": "Chicago Defender",
    "search_field": "mayor + lightfoot",
    "associated_candidate": "Lori Lightfoot",
    "site_id": "news_cd",
    "cand_id": "cand_ll",
}

def scrape_page(article_dict, url):
    """
    This function takes a URL to a page and returns a
    dictionary with the title, address, description,
    and history of the park.

    Parameters:
        * url:  a URL to a chicago defender page

    Returns:
        A dictionary with the following keys:
            * url:          the URL of the park page
            * name:         the name of the park
            * address:      the address of the park
            * description:  the description of the park
            * history:      the history of the park
    """
    html = make_s_request(url).text
    root = parse_html(html)

    return root

    article_dict['url'] = url

    # Should I make this lowercase? 
    article_dict['title'] = root.xpath("//h1")[0].text_content()
    
    body = root.xpath("//p")

    doc_text = ''
    for row in body[2:-3]:
        doc_text += row.text_content()
    
    article_dict['text'] = doc_text
    article_dict['date'] = root.xpath("//time")[0].text

    return article_dict

def parse_html(html):
    """
    Parse HTML and return the root node.
    """
    return lxml.html.fromstring(html)