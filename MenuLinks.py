import urllib2
from bs4 import BeautifulSoup
from requests import get
from urlparse import urljoin
from os import path, getcwd
from sys import argv
import os
import sys
import urllib2
import re
import urllib2
import urlparse
import requests
import os
import hashlib
from  collections  import deque
url = 'http://www.goldendragonindia.com/oriental-cuisine.html'
html=urllib2.urlopen(url).read()
soup = BeautifulSoup(html)
parsed_uri = urlparse.urlparse(url)
domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
for link in soup.find_all('img'):
    print domain + '/' + link['src']
