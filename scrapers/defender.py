import sys
import json
import lxml.html
import pandas as pd
from datetime import datetime
from utils import make_request, make_link_absolute


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
    html = make_request(url).text
    root = parse_html(html)

    page_dict = {}


    # Should I make this lowercase? 
    page_dict['title'] = root.xpath("//h1")[0].text_content()
    
    body = root.xpath("//p")

    doc_text = ''
    for row in body[2:-3]:
        doc_text += row
    
    page_dict['text'] = doc_text

    page_dict['date'] = root.xpath("//time")[0].text
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

def get_news_urls(search_string, stop_date, current_page = 1, url = "https://chicagodefender.com/page/"):
    """
    This function takes a URL to a page of parks and returns a
    list of URLs to each park on that page.

    Parameters:
        search_string: the string to append to the url to create the search
        url: the url to the chicago defender
        stop_date (datetime): the earliest date to include in searches

    Returns:
        A list of URLs to each park on the page.
    """

    # The string needs to be "mayor + associated_name", otherwise will fix here
    search = url + str(current_page) + "/?s=" + search_string

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
        date_list.append(datetime.strptime (day, '%B %d, %Y'))

    # Looping through the links on a page
    for i, link in enumerate(links):

        # Must have same number of links and dates
        if len(links) != len(dates):
            raise Exception("Dates and Links don't match")

        # Stopping Condition: Date is before candidate filed
        if date_list[i] < stop_date:
            return urls, False
        
        # Add URL to the list
        full_url = link.get("href")
        urls.append(full_url)

    return urls, True

def check_next_page_exists(search_string, current_page, url = "https://chicagodefender.com/page/"):
    """
    This function takes a URL to a page of search results and returns a
    URL to the next page of results if they exist.

    If no next page exists, this function returns None.
    """

    """OK so this function needs to pull the next page given the current page. 
    However, the location of the next page button is dependent on the current page
    Therefore, it may just make sense to modify the current url by tracking the 
    current page number and then replacing it with the next one

    """
    search = url + str(current_page) + "/?s=" + search_string

    html = make_request(search).text
    root = parse_html(html)

    nav_list = root.xpath("/html/body/div[1]/div/main//li")

    return len(nav_list)

def crawl(search_string, stop_date, article_dict, current_page = 1, 
            url="https://chicagodefender.com/page/"):
    """
    This function starts at the base URL for the parks site and
    crawls through each page of parks, scraping each park page
    and saving output to a file named "parks.json".

    Parameters:
        * max_parks_to_crawl:  the maximum number of pages to crawl
    """
    pages = []
    
    # Will continue in loop until get_next_page finds no next page
    while True:
        pages_to_add, status = get_news_urls(search_string, stop_date, current_page, url)

        for article in pages_to_add:
            pages.append(scrape_page(article_dict, article))

        cont = check_next_page_exists(search_string, current_page + 1, url)
        
        # If either we've crossed date limit or there are no more pages
        if not (cont and status):
            break
        
        current_page += 1

    print("Writing defender.json")
    with open("defender.json", "w") as f:
        json.dump(pages, f, indent=1)