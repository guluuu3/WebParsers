
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urlparse
from urlparse import urlsplit
from collections import deque
import re
import httplib2
import logging
import lxml
import hashlib
import urllib2
import requests
import logging
from raven import Client

""""
def LastModifiedCal(url):
    httplib2.debuglevel = 1
    h = httplib2.Http('.cache')
    response_last, content = h.request(url, headers={'cache-control':'no-cache'})
    if response_last.dict.has_key('last-modified'):
        return response_last('last-modified')
    else:
        return None

url = "stackoverflow.com,questions,15415709,update-json-file,bcd585a81bf2780ba8fca7324c3553a2"
print LastModifiedCal(url)

def LastModifiedCal(url):
    req = urllib2.urlopen(url)
    return  req.info().getheader('last-modified')
"""

def LastModifiedCal(url):
    r = httplib2.Http()
    response, _ = r.request(url, 'HEAD')
    try:
        return response.get('last-modified')
    except:
        return None











