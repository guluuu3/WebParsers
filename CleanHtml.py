import sys
import urllib2
import re
import urllib
import urlparse
import requests
import os
import hashlib
import re
import lxml
import json
import _json
import numpy
from  collections  import deque
from BeautifulSoup import BeautifulSoup
from urlparse import urlsplit
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urlparse
from urlparse import urlsplit
from collections import deque
from urllib import urlopen
import httplib2
import pymongo
from pymongo import MongoClient
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import lxml
import LatLongParser
import AddressParser
import PhoneNumberParser
import EmailParser
import LastModified
import SocialLinks
import FetchUrls
import threading
from multiprocessing.pool import ThreadPool
from urllib import quote
import OpeningClosingParser
import thread
import calendar
from datetime import datetime, timedelta
import calendar
from datetime import datetime, timedelta
from datetime import datetime
from time import mktime
from datetime import datetime
from dateutil import parser

def UtcToLocal(last_modified):
    dt = parser.parse(last_modified)
    timestamp = calendar.timegm(dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=dt.microsecond)

class PythonObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        return {'_python_object': pickle.dumps(obj).decode('latin1')}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(dct['_python_object'].encode('latin1'))
    return dct

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

def notNull(value):
    if len(value)!=0:
        return 1
    return 0

def MongoUpdateCal():
    client =  MongoClient()
    db =  client['parser']
    collection = db['parser']
    posts = db.posts
    return posts

def PushData(url,parent_url):

    new_urls = deque([url])
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    processed_urls = set()
    count  = 0
    while len(new_urls) and count < 10:
        count = count+1
        url = new_urls.popleft()
        processed_urls.add(url)
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url
        print("Processing %s" % url)

        try:
            response = requests.get(url)

        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        pool = ThreadPool(processes=7)
        email_result = pool.apply_async(EmailParser.EmailCall, (url,))
        social_link_result= pool.apply_async(SocialLinks.SocialLinksCal, (url,))
        latlong_result = pool.apply_async(LatLongParser.LatLongCal,(url,))
        address_result =  pool.apply_async(AddressParser.AddressCal,(url,))
        phone_number_result = pool.apply_async(PhoneNumberParser.PhoneNumberCal,(url,))
        last_modified_result  = pool.apply_async(LastModified.LastModifiedCal,(url,))
        opening_closing_result = pool.apply_async(OpeningClosingParser.OpeningClosingCal,(url,))


        latlong = latlong_result.get()
        emails = email_result.get()
        address = address_result.get()
        phone_number = phone_number_result.get()
        last_modified = last_modified_result.get()
        social_link = social_link_result.get()
        opening_closing =  opening_closing_result.get()

        posts = MongoUpdateCal()
        data = {}

        data["url"] = url

        if latlong != None:
            latlong = latlong.split(',')
            latitude = latlong[0]
            longitude = latlong[1]
            data['latitude'] = latitude
            data['longitude'] = longitude

        else:
            latlong_values = None
            latitude = None
            longitude = None

        if len(emails) != 0:
            data["email"] = emails

        if len(phone_number) != 0:
            data["phone_number"] = phone_number

        if len(address) != 0:
            data["address"] = address
            print address

        if len(opening_closing) != 0:
            data["timings"] = opening_closing

        if last_modified != None:
            last_modified = UtcToLocal(last_modified)
            data["last_modified"] = last_modified

        if social_link != None:
            data["social_links"] = social_link

        parent_data = {'parent_url': parent_url, 'child': data}
        posts.insert(parent_data)
        """
        with open("data.json", mode='w') as f:
            json.dump([], f,default=jdefault)

        with open("data.json", "a") as json_file:
            json_file.write("{}\n".format(json.dump(parent_data, json_file,default=jdefault)))
        """
        soup = BeautifulSoup(response.text, 'lxml')

        for anchor in soup.find_all("a"):
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in new_urls and not link in processed_urls:
                parsed_link = urlparse.urlparse(link)
                link_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_link)
                if link_domain == domain:
                    if "#"  not in link:
                        new_urls.append(link)


url ="http://www.2for1pizzala.com/"
PushData(url,url)
#FetchUrls.MongoUpdateToSql(url)
"""
with open("data.txt") as code:
    for restaurants_url in code:
        res_name_ = restaurants_url.split(',')[0]
        res_url_ = restaurants_url.split(',')[-1]
        res_name = res_name_[1:-1]
        res_url = res_url_[1:-2]
        PushData(res_url,res_url)
        #FetchUrls.MongoUpdateToSql(res_url)
"""



