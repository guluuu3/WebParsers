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
import mysql.connector
from mysql.connector import Error
import pymongo
from pymongo import MongoClient

def InsertInCrawlWebsite(res_name ,url):
    conn = mysql.connector.connect(host='10.0.126.129',database='zomato_content' ,user='foodie_read' , password='zooF4cie')
    try:
        if conn.is_connected():
            cursor  = conn.cursor()
            insertstmt="insert into crawl_website ( res_name ,url, parser_flag) values ('{res_name_}', '{url_}', {flag_})"\
                .format(res_name_= res_name, url_ = url , flag_  = 0 )
            cursor.execute(insertstmt)
            print insertstmt
            conn.commit()
        else:
            print 'Connect first '
    except:
        print "not found"


def InsertInCrawlDataWebsite(parent_url ,child_url,key,value):
    print child_url,value
    conn = mysql.connector.connect(host='10.0.126.129',database='zomato_content' ,user='foodie_read' , password='zooF4cie')
    #if InsertUniqueFromMongo(parent_url,key,value)== True:
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            str = ""
            str = "insert ignore into crawl_data_website( `parent_res_url` , `child_res_url` , `key` , `value_`) values ( "
            str += " ' " + parent_url + " '  , ' " + child_url + " ' , ' " + key + " ' , ' " + value + " ' )"
            cursor.execute(str)
            conn.commit()
        else:
            return
    except:
        return


def UrlsCal():
    conn = mysql.connector.connect(host='10.0.126.129',database='zomato_content' ,user='foodie_read' , password='zooF4cie')
    try:
        cursor  = conn.cursor()
        insertstmt="select url FROM crawl_website"
        cursor.execute(insertstmt)
        row = cursor.fetchall()
        return row
    except:
        return None

def ReadFromFile():
    with open("urls.txt") as code:
        for restaurants_url in code:
            res_name =  restaurants_url.split(',')[0]
            res_url= restaurants_url.split(',')[-1]
            #print res_url
            res_name = res_name[1:-1]
            res_url = res_url[1:-2]
            InsertInCrawlWebsite(res_name ,res_url)

def ConvertListToString(value):
    new_string = ""
    for values in value:
                new_string += values + " , "
    new_string = new_string[:-2]
    return new_string

def PullValuesFromMongo(key,dictionary):
    if key in dictionary:
        key_string = dictionary[key]
        return key_string
    return None

def InsertUniqueFromMongo(parent_url,keys,values):
    #print parent_url,keys,values
    conn = mysql.connector.connect(host='10.0.126.129',database='zomato_content' ,user='foodie_read' , password='zooF4cie')
    try:
        cursor = conn.cursor()
        insertstmt = 'select `parent_res_url`, `child_res_url` FROM crawl_data_website where `parent_res_url`  LIKE "%{parent_url_}%" and `value_` LIKE "%{values_}%" '.format(parent_url_=parent_url, values_=values)
        cursor.execute(insertstmt)
        row = cursor.fetchall()
        if len(row)==0:
            return True
        else:
            return False
    except:
        return None
def MongoUpdateToSql(parent_url):
    client =  MongoClient()
    db =  client['parser']
    collection = db['parser']
    posts = db.posts
    result = collection.find()

    for child in db.posts.find({"parent_url" : parent_url}):

        child_url = child['child']['url']

        email = PullValuesFromMongo("email",child["child"])
        if email!= None:
            email_string =  ConvertListToString(email)
            InsertInCrawlDataWebsite(parent_url,child_url,"email",email_string)

        phone_number = PullValuesFromMongo("phone_number",child["child"])
        if phone_number!= None:
            phone_string =  ConvertListToString(phone_number)
            InsertInCrawlDataWebsite(parent_url,child_url,"phone",phone_string)


        if "address" in child["child"]:
            key = "address"
            value  = child['child']['address']
            for address_string in value:
                if len(address_string)>10:
                    #if InsertUniqueFromMongo(parent_url,key,address_string)== True:
                    InsertInCrawlDataWebsite(parent_url,child_url,key,address_string)

        if "timings" in child["child"]:
            key = "timings"
            value  = child['child']['timings']
            for timings_string in value:
                if len(timings_string)>10:
                    #if InsertUniqueFromMongo(parent_url,key,timings_string)== True:
                    InsertInCrawlDataWebsite(parent_url,child_url,key,timings_string)

        if "social_links" in child['child']:

            facebook_string = PullValuesFromMongo("facebook__link",child['child']['social_links'])
            if facebook_string!= None:
                InsertInCrawlDataWebsite(parent_url,child_url,"facebook_website",facebook_string)

            twitter_string = PullValuesFromMongo("twitter_link",child['child']['social_links'])
            if twitter_string!= None:
                InsertInCrawlDataWebsite(parent_url,child_url,"twitter_website",twitter_string)

            instagram_string = PullValuesFromMongo("instagram_link",child['child']['social_links'])
            if instagram_string!= None:
                InsertInCrawlDataWebsite(parent_url,child_url,"instagram_website",instagram_string)

            google_plus_string = PullValuesFromMongo("google_plus_link",child['child']['social_links'])
            if google_plus_string!= None:
                InsertInCrawlDataWebsite(parent_url,child_url,"google_plus_website",google_plus_string)

            youtube_string = PullValuesFromMongo("youtube_link",child['child']['social_links'])
            if youtube_string!= None:
                InsertInCrawlDataWebsite(parent_url,child_url,"youtube_website",youtube_string)

        latitude_string = PullValuesFromMongo("latitude",child['child'])
        if latitude_string!=None:
            InsertInCrawlDataWebsite(parent_url,child_url,"latitude",latitude_string)

        longitude_string  = PullValuesFromMongo("longitude",child["child"])
        if longitude_string!=None:
            InsertInCrawlDataWebsite(parent_url,child_url,"longitude",longitude_string)

        last_modified_string = PullValuesFromMongo("last_modified",child["child"])
        if last_modified_string!=None:
            InsertInCrawlDataWebsite(parent_url,child_url,"last_modified",last_modified_string)

#parent_url ="http://www.2for1pizzala.com/"
#MongoUpdateToSql(parent_url)
#InsertUniqueFromMongo()

with open("data.txt") as code:
    for restaurants_url in code:
        res_name_ = restaurants_url.split(',')[0]
        res_url_ = restaurants_url.split(',')[-1]
        res_name = res_name_[1:-1]
        res_url = res_url_[1:-2]
        #PushData(res_url,res_url)
        MongoUpdateToSql(res_url)









