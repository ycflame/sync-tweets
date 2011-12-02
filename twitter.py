#!/usr/bin/env python
# -*- coding: utf-8 -*-

#to ensure the utf8 encoding environment
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import base64
import re
import htmlentitydefs
import time
import urllib,urllib2,Cookie
import oauth2 as oauth
from google.appengine.api import urlfetch
from google.appengine.ext import db

class Twitter(db.Model):
    id=db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

def make_cookie_header(cookie):
    ret = ""
    for val in cookie.values():
        ret+="%s=%s; "%(val.key, val.value)
    return ret

def unescape(text):
   """Removes HTML or XML character references 
      and entities from a text string.
   from Fredrik Lundh
   http://effbot.org/zone/re-sub.htm#unescape-html
   """
   def fixup(m):
       text = m.group(0)
       if text[:2] == "&#":
           # character reference
           try:
               if text[:3] == "&#x":
                   return unichr(int(text[3:-1], 16))
               else:
                   return unichr(int(text[2:-1]))
           except ValueError:
               pass
       else:
           # named entity
           try:
               text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
           except KeyError:
               pass
       return text # leave as is
   return re.sub("&#?\w+;", fixup, text)

def getLatest():
    msg=db.GqlQuery("SELECT * FROM Twitter ORDER BY created DESC")
    x=msg.count()
    if x:
        return msg[0].id
    else:
        return ""

def send_fanfou_msgs(msg):
	consumer = oauth.Consumer(key="your_consumer_key", secret="your_consumer_secret")
	token = oauth.Token(key="your_access_token", secret="your_access_secret")
	post_url = "http://api.fanfou.com/statuses/update.json"

	client = oauth.Client(consumer, token)
	msg=unescape(msg)
	form_fields = {
			"status": msg
			}
	form_data = urllib.urlencode(form_fields)
	client.request(post_url, "POST", form_data)
	
def send_digu_msgs(username,password,msg):
	auth=base64.b64encode(username+":"+password)
	auth='Basic '+auth
	msg=unescape(msg)
	form_fields = {
			"content": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://api.minicloud.com.cn/statuses/update.format",
			payload=form_data,
			method=urlfetch.POST,
			headers={'Authorization':auth}
			)
	if result.status_code == 200:
		bk=result.content
		if bk.find("true"):
			return True
	else:
		return False

#get one page of to user's replies, 20 messages at most. 
def parseTwitter(twitter_id,since_id="",):
    if since_id:
        url="http://twitter.com/statuses/user_timeline/%s.xml?since_id=%s"%(twitter_id,since_id)
    else:
        url="http://twitter.com/statuses/user_timeline/%s.xml"%(twitter_id)
    #print url
    result = urlfetch.fetch(url)
    #print result.content
    if result.status_code == 200:
        content=result.content
        m= re.findall(r"(?i)<id>([^<]+)</id>\s*<text>(?!@)([^<]+)</text>", content)
	print "<html><body><ol>"
	for x in reversed(m):
		id=x[0]
		text=x[1]
		if text.find('@') == -1 :
			print "<li>",id,text,"</li><br />\n"
			# find all t.co links 
			urls = re.findall("http\S+",text) 
			# if find some 
			if len(urls)!=0: 
				for url in urls: 
					# construct the new link 
					suburl = re.sub("t.co","233.im/tco.php",url) 
					content = urllib2.urlopen(suburl).read() 
					# get the origin link 
					result = re.search("http\S+",content) 
					# substitute the t.co link in the tweets 
					text = re.sub(url,result.group(0),text)
# You MUST modify your username and password here ##############################################
			ret = send_digu_msgs("username","password",text)
			send_fanfou_msgs(text)
			msg=Twitter()
			msg.id=id
			msg.put()
	print "</ol></body></html>"
    else:
        print "get twitter data error. "
	print result.content
        
print ""
latest=getLatest() 
# You MUST modify your twitter username  here ##################################################
parseTwitter(twitter_id="username",since_id=latest)
