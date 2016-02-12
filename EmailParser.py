from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urlparse
from urlparse import urlsplit
from collections import deque
import re
import numpy as np


def EmailCall(url):
    emails = set()
    updated_emails = []
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        return
    new_emails =(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    for new_email in new_emails:
        emails.add(new_email)
    for email in emails:
        updated_emails.append(email)
    np.unique(emails)
    return  updated_emails