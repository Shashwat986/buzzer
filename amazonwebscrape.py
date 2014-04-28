import sys
import re
import json
import urllib
import urllib2
import urlparse
from bs4 import BeautifulSoup
from pprint import pprint
import codecs
from bs4 import Comment
import bottlenose
import sentiment

azCache = {}

keyword = "IPhone 5C"

def connect(url):
	try:
		user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		
		headers={'User-Agent':user_agent,} 
		request=urllib2.Request(url,None,headers)
		response = urllib2.urlopen(request)
	except Exception, e:
		print "Connection Failed.",e
		return ""

	msg=response.read()
	return msg

def getAccessToken() :

	myAWSId = 'Yout-AWS-ID'
	myAWSSecret = 'AWS-Secret'
	myEndPoint = 'AWS-Endpoint'

	amazon = bottlenose.Amazon(myAWSId, myAWSSecret, Version="2009-10-01")
        return amazon
        
def amazon(amazon, keyword):

        if keyword in azCache:
                return azCache[keyword]

	prodASIN = BeautifulSoup(amazon.ItemSearch(Keywords = keyword, SearchIndex = "All", AssociateTag = "Random")).item.asin.string

	url = BeautifulSoup(amazon.ItemLookup(ItemId = prodASIN, IdType = "ASIN", ResponseGroup = "Reviews", AssociateTag = "Random")).iframeurl.string

	soup = BeautifulSoup(connect(url))
        try:
                url = soup.find(class_ = "crIFrameNumCustReviews").a['href']        
                soup = BeautifulSoup(connect(url))
        except:
                pass
        
	comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        print url
	v = []
	for k in comments:
		if "BOUNDARY" not in k:
			continue
		try:
			v.append(k.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling)
		except:
			pass

	ans = {}
	ans["data"]=[]
	for k in v:
		try:
                        wt = int(k.find_all('div')[0].get_text().encode('ascii','ignore').strip().split()[0])
		
                        nm = k.find_all('div')[2].find('a').string.encode('ascii','ignore').strip()                        
			location = k.find_all('div')[2].get_text().split("(")[1].split(")")[0]

                        for tag in k.find_all():
                                tag.decompose()
                        review = k.get_text().strip()
                except:
			continue
		temp = {}
                s=sentiment.sentiment(review,keyword)
		temp["text"] = review
		temp["name"] = nm
		temp["location"] = location
		r = connect("http://dev.virtualearth.net/REST/v1/Locations?query=" + urllib.quote(location) + "&output=json&key=Ar31XPc8UKrmZMDPsEVNjdAcz4yyfLtrqAkSKrNnd-RQVpFUqz4xZH1UqqTOraQI")
		d = json.loads(r)
		try: temp["lat"] = d['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
		except: temp["lat"] = ""
		
		try: temp["long"] = d['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
		except: temp["long"] = ""
		
		temp["weight"] = wt
                temp["sentiment"]=s
                temp["userid"]=s
                
		ans["data"].append(temp)
	data2 = sorted(ans['data'], key = lambda user: user['weight'],reverse=True)
	ans["data"]=data2
        azCache[keyword] = ans
	return ans
#'''
