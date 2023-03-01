"""
Author: Lee-Or Bentovim
Last Modified: 2/25/23

This file is drawn directly from the utility file we were given in PA2, modified
for use with non scrapple pages.
"""

import time
import requests
from urllib.parse import urlparse

REQUEST_DELAY = 0.1


def make_request(url):
    """
    Make a request to `url` and return the raw response.
    """
    time.sleep(REQUEST_DELAY)
    print(f"Fetching {url}")
    hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
    resp = requests.get(url, headers = hdr)
    return resp
