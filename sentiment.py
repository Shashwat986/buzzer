import urllib2
import urllib
from random import choice

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

def sentiment(text, target):
	keys = ['5f40995d8dc06c85f02df93a5b370ec744590669',
		'364dff5755880f9d141b88b7c67c5281e848ff65',
		'7bf525e6380852a78add5f1ff3cb4a1aec5213a3']
        text = ''.join(ch for ch in text if ch.isalnum() or ch == " ")
        target = ''.join(ch for ch in target if ch.isalnum() or ch == " ")
        try:
                url = "http://access.alchemyapi.com/calls/text/TextGetTargetedSentiment?"+ urllib.urlencode({'text':text, 'apikey':choice(keys), 'target':target})
                msg = connect(url)                                                
        except Exception, e:
                print e
                msg = 'neutral'
	if "neutral" in msg:
		return 0
	elif "negative" in msg:
		return -1
	elif "positive" in msg:
		return 1
	return 0
