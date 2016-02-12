import urllib
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urlparse
import urllib
import urllib2
from urlparse import urlsplit
from collections import deque
import re
import numpy as np
from  more_itertools import unique_everseen
import lxml

address = set()

def CleanText(text):
    for script in text(['style' ,'script', '[document]', 'head', 'title']):
                script.extract()

    text = text.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def cleanMe(html):
    soup = BeautifulSoup(html) # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def StripAddress(text,match):
    index = text.find(match.group(0))
    text = text[0:index+10]
    if len(text)>110:
        text= text[index-90:]
    return text

def SearchInDivSpanByPin(pin_code_path, html):
    soup = BeautifulSoup(html)
    with open(pin_code_path) as fp:
            for pattern in fp:
                try:
                    for s in soup.findAll("div"):
                        for p in s.find_all('span'):
                            #print p.get_text()
                            if len(p) != 0:
                                for match in re.finditer(pattern, p.get_text()):
                                    if match:
                                        #print "pin", pattern
                                        text = CleanText(p)
                                        text = StripAddress(text, match)
                                        address.add(text)
                except:
                    return


def SearchInDivSpanByPhone(phone_code_path, html):
    soup = BeautifulSoup(html)
    with open(phone_code_path) as fp:
            for pattern in fp:
                try:
                    for s in soup.findAll("div"):
                        for p in s.find_all('span'):
                            if len(p) != 0:
                                for match in re.finditer(pattern, p.get_text()):
                                    if match:
                                        #print "pin", pattern
                                        text = CleanText(p)
                                        text = StripAddress(text, match)
                                        address.add(text)
                except:
                    return

def SearchInDivByPin(pin_code_path, html):
    soup = BeautifulSoup(html)
    with open(pin_code_path) as fp:
            for pattern in fp:
                try:
                    for p in soup.findAll("div"):
                        if len(p)!=0:
                            for match in re.finditer(pattern, p.get_text()):
                                if match:
                                    #print "pin",pattern
                                    text = CleanText(p)
                                    text = StripAddress(text,match)
                                    address.add(text)
                except:
                    return

def SearchInDivByPhone(phone_code_path, html):
    soup = BeautifulSoup(html)
    with open(phone_code_path) as fp:
            for pattern in fp:
                try:
                    for p in soup.findAll("div"):
                        if len(p)!=0:
                            for match in re.finditer(pattern, p.get_text()):
                                if match:
                                    #print "phone"
                                    text = CleanText(p)
                                    text = StripAddress(text,match)
                                    address.add(text)
                except:
                    return


def SearchDivAndParaByPhone(phone_code_path, html):
    soup = BeautifulSoup(html)
    with open(phone_code_path) as fp:
        for pattern in fp:
            try:
                for p in soup.find('div').find_all("p"):
                    if len(p)!= 0:
                        for match in re.finditer(pattern, p.get_text()):
                            if match:
                                #print "phone_p"
                                text = CleanText(p)
                                text = StripAddress(text,match)
                                address.add(text)
            except:
                return


def SearchDivAndParaByPin(pin_code_path, html):
    soup = BeautifulSoup(html)
    with open(pin_code_path) as fp:
        for pattern in fp:
            try:
                for p in soup.find('div').find_all("p"):
                    if len(p)!=0:
                        for match in re.finditer(pattern, p.get_text()):
                            if match:
                                #print "pin_p"
                                text = CleanText(p)
                                text = StripAddress(text,match)
                                address.add(text)
            except:
                return

def SearchDivAndClassByPin(pin_code_path, html):
    soup = BeautifulSoup(html)
    with open(pin_code_path) as fp:
        for pattern in fp:
            try:
                for classes in soup.findAll('div'):
                    for p in classes.findAll('p'):
                        if len(p)!=0:
                            for match in re.finditer(pattern, p.get_text()):
                                if match:
                                    #print "pin_c"
                                    text = CleanText(p)
                                    text = StripAddress(text,match)
                                    address.add(text)
            except:
                return

def SearchDivAndClassByPhone(phone_code_path, html):
    soup = BeautifulSoup(html)
    with open(phone_code_path) as fp:
        for pattern in fp:
            try:
                for classes in soup.findAll('div'):
                    for p in classes.findAll('p'):
                        if len(p)!=0:
                            for match in re.finditer(pattern, p.get_text()):
                                if match:
                                    #print "phone_c"
                                    text = CleanText(p)
                                    text = StripAddress(text,match)
                                    address.add(text)
            except:
                return


def SearchTableByPhone(phone_code_path, html):
    soup = BeautifulSoup(html)
    with open(phone_code_path) as fp:
        for pattern in fp:
            try:
                for p in soup.findAll("table"):
                    if len(p)!=0:
                        for match in re.finditer(pattern, p.get_text()):
                            if match:
                                #print "phone_t"
                                text = CleanText(p)
                                text = StripAddress(text,match)
                                address.add(text)
            except:
                return

def SearchTableByPin(pin_code_path, html):
    soup = BeautifulSoup(html)
    with open(pin_code_path) as fp:
        for pattern in fp:
            try:
                for p in soup.findAll("table"):
                    if len(p )!= 0:
                        for match in re.finditer(pattern, p.get_text()):
                            if match:
                                #print "pin_t"
                                text = CleanText(p)
                                text = StripAddress(text,match)
                                address.add(text)
            except:
                return

def SearchOpenTextPhone(phone_code_path, html):
    text = cleanMe(html)
    with open(phone_code_path) as fp:
        for pattern in fp:
            try:
                m = re.search(pattern, text)
                if m:
                    print "***********************************"
                    print(m.group(0))
            except:
                return

def SearchOpenTextPin(pin_code_path, html):
    text = cleanMe(html)
    with open(pin_code_path) as fp:
        for pattern in fp:
            try:
                m = re.search(pattern, text)
                if m:
                    print "************************************"
                    print(m.group(0))
            except:
                return



def AddressCal(url):
    address_list = []
    try:
        html = urllib.urlopen(url).read()
    except:
        return address_list
    pin_code_path = "AddressRegex.txt"
    phone_code_path = "PhoneRegex.txt"
    #SearchOpenTextPhone(phone_code_path, html)
    #SearchOpenTextPin(pin_code_path,html)
    SearchInDivSpanByPin(phone_code_path,html)
    SearchDivAndClassByPhone(phone_code_path,html)
    SearchInDivByPin(pin_code_path, html)
    SearchInDivByPhone(phone_code_path,html)
    SearchDivAndParaByPhone(phone_code_path, html)
    SearchDivAndClassByPin(pin_code_path,html)
    SearchDivAndClassByPhone(phone_code_path, html)
    SearchDivAndParaByPin(pin_code_path,html)
    SearchTableByPhone(phone_code_path, html)
    SearchTableByPin(pin_code_path, html)
    for x in  address:
        address_list.append(x)
    np.unique(address_list)
    with open("en.txt") as code:
        for word in code:
            matching = [s for s in address_list if word in s]
            for match in matching:
                if len(address_list)!=0:
                    address_list.remove(match)
    address.clear()
    return address_list