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

def  FacebookLink(current_link):
    pattern_search = re.compile("facebook")
    matches = pattern_search.search(current_link)
    if matches:
        return current_link
    return None

def  TwitterLink(current_link):
    pattern_search = re.compile("twitter")
    matches = pattern_search.search(current_link)
    if matches:
        return current_link
    return None

def  InstagramLink(current_link):
    pattern_search = re.compile("instagram")
    matches = pattern_search.search(current_link)
    if matches:
        return current_link
    return None

def  GooglePlusLink(current_link):
    pattern_search = re.compile("plus.google")
    matches = pattern_search.search(current_link)
    if matches:
        return current_link
    return None

def  YoutubeLink(current_link):
    pattern_search = re.compile("youtube")
    matches = pattern_search.search(current_link)
    if matches:
        return current_link
    return None


def SocialLinksCal(url):
    try:
        html=urllib2.urlopen(url).read()
    except:
        return None
    soup = BeautifulSoup(html)
    current_link = ''
    social_links = {}
    for link in soup.find_all('a'):
      try:
          current_link = link.get('href')
          facebook_link = FacebookLink(current_link)
          twitter_link = TwitterLink(current_link)
          instagram_link = InstagramLink(current_link)
          google_plus_link = GooglePlusLink(current_link)
          youtube_link = YoutubeLink(current_link)

          if facebook_link != None:
              social_links["facebook_link"] =facebook_link

          if twitter_link !=None:
              social_links["twitter_link"] = twitter_link

          if instagram_link != None:
              social_links['instagram_link'] = instagram_link

          if google_plus_link != None:
              social_links['google_plus_link'] = google_plus_link

          if youtube_link != None:
              social_links['youtube_link'] = youtube_link
      except:
          return None

    return  social_links
