from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urlparse
from urlparse import urlsplit
from collections import deque
import re
import lxml
import hashlib

def LatLongCal(url):
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        return
    soup=BeautifulSoup(response.text,'lxml')
    latlong = set()
    for scores_string in soup.find_all('a', href=re.compile('(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+))')):
        if len(scores_string)!=0:
           latlong = str(scores_string['href'])
           pattern_search = re.compile("(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+))")
           matches = pattern_search.search(latlong)
           if matches:
               return matches.group(0)

    return None

