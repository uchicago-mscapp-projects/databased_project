import sys
import json
import lxml.html
import datetime 
from datetime import datetime
#from .utils import make_request, make_link_absolute


def scrape_park_page(full_name, announcement_date):
    # Assumming passed in date is a date object

    # Retreive correct search url
    current_url = get_first_search_page(full_name) 
    after_announcement = True
    list_of_article_urls = []
    list_of_scraped_pages = []

    while(current_url and after_announcement): 
        # Scrape pages
        article_urls, after_announcement = get_article_urls(current_url, announcement_date)
        list_of_article_urls. append(article_urls)
        current_url = get_next_page(current_url)
    print(list_of_article_urls)
    
    # Scrape all pages
    for page_url in list_of_article_urls:
        page_dict = scrape_article(page_url[0])
        list_of_scraped_pages.append(page_dict)
    
    print(list_of_scraped_pages)

def get_first_search_page(full_name):
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
            print("$"+date.text_content()+"$")
            parsed_date = date_convert(date.text_content())
            if parsed_date < announcement_date:
                # Article was written prior to announcement
                return urls, False

            article_url = article[0].cssselect("a")[0].get("href")

            urls.append(article_url)
       
    return urls, True

def get_next_page(url):
    # TODO maybe pass the root node
    page = make_request(url)
    root = lxml.html.fromstring(page.text)

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
        # Page has changed
        raise Exception ("Page has changed: check next link buttons/structure")

def scrape_article(url):
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
    
    parsed_date = date_convert(date)

    # Get article text 
    full_text = article[0].cssselect("div")[2].cssselect("p")[0].text_content()

    # pass in the missing args? 
    full_article = {
        'website_title' : "Lawndale News",
        'url' : url,
        'search_field' : None,
        'article_title' : title,
        'article_text' : full_text,
        'associated_candidate' : None,
        'publication_date' : parsed_date,
        'site_id' : None,
        'cand_id' : None
    }

    return full_article

def date_convert(date):
    try:
        parsed_date = datetime.strptime(date, '%B %d, %Y')
        return parsed_date
    except TypeError:
        raise("Error in date parsing: Format has changed. Type Error")
    except ValueError:
        raise("Error in date parsing: Format has changed. Value Error")
    except: 
        raise("Error in date parsing: Format has changed.")
       

    
