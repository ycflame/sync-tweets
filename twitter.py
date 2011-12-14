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
import simplejson as json
from google.appengine.api import urlfetch
from google.appengine.ext import db

class TweetID(db.Model):
	id=db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)

def getLatest():
	msg=db.GqlQuery("SELECT * FROM TweetID ORDER BY created DESC")
	x=msg.count()
	if x:
		return msg[0].id
	else:
		return ""

def send_fanfou_msgs(msg):
	consumer = oauth.Consumer(key="52b62bd6315d823a32bcfe4dfaa40119", secret="62189cb88e31febd707cb8337231e18a")
	token = oauth.Token(key="your_access_token", secret="your_access_key")
	post_url = "http://api.fanfou.com/statuses/update.json"

	client = oauth.Client(consumer, token)
	form_fields = {
			"status": msg
			}
	form_data = urllib.urlencode(form_fields)
	client.request(post_url, "POST", form_data)

def send_digu_msgs(username,password,msg):
	auth=base64.b64encode(username+":"+password)
	auth='Basic '+auth
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

# get one page of to user's replies, 20 messages at most. 
def oauth_req(url, http_method="GET"):
	consumer = oauth.Consumer(key='your_consumer_key', secret='your_consumer_secret')
	token = oauth.Token(key='your_access_token', secret='your_access_token_secret')
	client = oauth.Client(consumer, token)

	resp, content = client.request(url, method=http_method)
	return resp, content


def getTweets(twitter_id,since_id=""):
	url = "http://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&exclude_replies=true&screen_name=%s" % twitter_id
	if since_id:
		url += "&since_id=%s" % since_id
    #print url
	result, content = oauth_req(url)
	if result['status'] != '200':
		    raise Exception("Invalid response %s." % result['status'])
	else:
		tweets = json.loads(content)
		for tweet in reversed(tweets):
			id=tweet['id_str']
			text=tweet['text']
			urls = tweet['entities']['urls']
			# if find some
			if len(urls)!=0:
				for url in urls:
					# get the origin link
					origin = url['display_url']
					wrapped = url['url']
					# substitute the t.co link in the tweets 
					text = re.sub(wrapped,origin,text)

			send_fanfou_msgs(text)
# You MUST modify your username and password here ##############################################
			ret = send_digu_msgs("username","password",text)
			msg=TweetID()
			msg.id=id
			msg.put()
#get the since_id
latest=getLatest()
# You MUST modify your twitter username  here ##################################################
getTweets(twitter_id="username",since_id=latest)
