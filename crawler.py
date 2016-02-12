import sys
import urllib2
import re
import urllib2
import urlparse
import requests
import os
import hashlib
from  collections  import deque
from BeautifulSoup import BeautifulSoup



linkregex = re.compile(r'<a.*?href=[\'|"]?(.*?)[\'|"]?\s*>', re.IGNORECASE)
search_depth = 5

class Crawler(object):

    def __init__(self,root,depth):
        self.root=root
        self.depth=depth
        self.host=urlparse.urlparse(self.root).netloc
        self.crawled=[]
        self.uncrawled=[]
        self.externalLinks=[]
        self.links=1

    def crawl(self):
        page=GetLinks(self.root)
        childQ=deque()
        parentQ=deque()
        parentQ.append(self.root)
        level=0
        while(True):
            try:
                url=parentQ.popleft()
            except:
                level=level+1
                print("\n")
                if level ==self.depth:
                    break
                else:
                    while childQ:
                        url=childQ.popleft()
                        parentQ.append(url)
                    if not parentQ:
                        print "No more links"
                        print "Finishing"
                        break
                    else:
                        continue

            if url not in self.crawled:
                try:
                    host=urlparse.urlparse(url).netloc
                    if re.match(".*%s" % self.host,host):
                        self.links+=1
                        self.crawled.append(url)
                        page= GetLinks(url)
                        page.get()
                        for new_urls in page.urls:
                            if new_urls not in self.crawled:
                                childQ.append(new_urls)
                    else:
                        self.externalLinks.append(url)

                except Exception, e:
                    print "ERROR :Cants process links"
        while childQ:
            link = childQ.popleft()
            self.uncrawled.append(link)

class GetLinks(object):

    def __init__(self,url):
        self.url=url
        self.urls=[]

    def get(self):
        url=urlparse.urlparse(self.url)
        request=urllib2.Request(self.url)
        response=urllib2.urlopen(request)
        page=response.read()
        soup=BeautifulSoup(page)
        tags=soup('a')
        crawled_all = set()
        for tag in tags:
            link= tag.get("href")
            link = str(link)
            if link.startswith('/'):
                link=url.scheme + '://' +url.netloc + link
                crawled_all.add(link)
            elif not link.startswith('https'):
                link = 'http://' + url[1] + '/' + link
                crawled_all.add(link)
        start_index = 0
        for links in crawled_all:
            parsed_uri = urlparse.urlparse(links)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            domain = domain.replace("https://","")
            domain = domain.replace("www.", "")
            domain = domain.replace("http://","")
            length = len(links)
            #print length
            f = urllib2.urlopen(links)
            #url shortening and making it unique
            url_name = hashlib.md5(links.encode('utf-8')).hexdigest()
            directory = "dir/" + domain
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_name = directory + '/' + url_name + '.html'
            start_index  = start_index + 1
            with open(file_name, "wb") as code:
                if not os.path.isdir(file_name):
                    code.write(f.read())
def main():
    #if len(sys.argv) < 2:
        #print 'No start url was given'
        #sys.exit()

    #url = sys.argv[1]
    with open('urls.txt') as openfileobject:
        for url in openfileobject:
            print "Crawling %s (Max Depth: %d)" % (url, search_depth)
            crawler = Crawler(url,search_depth)
            crawler.crawl()
            print "Total internal links found " + str(crawler.links)
            print "Total links crawled " + str(len(crawler.crawled))
            print "\nUncrawled links "
            print "\n".join(crawler.uncrawled)
            print "\nExternal links:"
            print "\n".join(crawler.externalLinks)
if __name__ == "__main__":
    main()