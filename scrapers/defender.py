import sys
import json
import lxml.html
from .utils import make_request, make_link_absolute


def scrape_park_page(url):
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
    html = make_request(url).text
    root = parse_html(html)

    page_dict = {}

    page_dict['date'] = root.xpath("//time")[0].text

    # if page_dict['date'] before DATE RAISE: Except: Date Outside Range

    # Should I make this lowercase? 
    page_dict['title'] = root.xpath("//h1")[0].text_content()
    
    body = root.xpath("//p")

    doc_text = ''
    for row in body[2:-3]:
        doc_text += row
    
    page_dict['text'] = doc_text

    """
    Website Title (string) Comes pre-filled
    URL (string): URL
    Search Field: Comes pre-filled
    Title (string): done
    Text (string): done
    Associated Candidate (string): pre-filled
    Publication Date (date): done
    Tags (string): None
    Site ID - foreign key
    Cand ID - foreign key
    """

    return root



def parse_html(html):
    """
    Parse HTML and return the root node.
    """
    return lxml.html.fromstring(html)

def get_park_urls(search_string, url, stop_date):
    """
    This function takes a URL to a page of parks and returns a
    list of URLs to each park on that page.

    Parameters:
        * url:  a URL to a page of parks

    Returns:
        A list of URLs to each park on the page.
    """
    urls = []

    html = make_request(url).text
    root = parse_html(html)

    return root

    links = root.xpath("//tbody//a")

    for link in links:
        short_url = link.get("href")
        full_url = make_link_absolute(short_url,url)
        urls.append(full_url)

    return urls