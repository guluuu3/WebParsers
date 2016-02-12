from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urlparse
from urlparse import urlsplit
from collections import deque
import re
import lxml
import hashlib
import numpy as np
from  more_itertools import unique_everseen

def PhoneNumberCal(url):
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        return
    soup=BeautifulSoup(response.text,'lxml')
    phone_number = set()
    phone_list = []
    flag = False
    with open('PhoneRegex.txt') as fp:
        for pattern in fp:
            for match in re.finditer(pattern, response.text):
                if match:
                    phone_number.add(match.group(0))
    for phones in phone_number:
        phone_list.append(phones)
    return phone_list




