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

def PdfDownloadCal(url):
    html=urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    current_link = ''
    for link in soup.find_all('a'):
      current_link = link.get('href')
      if current_link.endswith('.pdf'):
          parsed_uri = urlparse.urlparse(current_link)
          domain_pdf = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
          domain_pdf = domain_pdf.replace("https://","")
          domain_pdf = domain_pdf.replace("www.", "")
          domain_pdf = domain_pdf.replace("http://","")
          directory = "pdfs/" + domain_pdf
          url_name = hashlib.md5(current_link.encode('utf-8')).hexdigest()
          f = urllib2.urlopen(current_link)
          if not os.path.exists(directory):
              os.makedirs(directory)
          file_name = directory + '/' + url_name + '.pdf'
          with open(file_name, "wb") as code:
                  code.write(f.read())