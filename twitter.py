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
	token = oauth.Token(key="585259-1266884a0e5b978288c4aff07c9805d1", secret="cc69a9d029cdea000ebfc52e9c2119c8")
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
	consumer = oauth.Consumer(key='4a9XAhTs4KDcc5DPuw27A', secret='HyJUY8AOQ9JP2mX5n6keRb68WSwPg3lA63Gmk5uVc')
	token = oauth.Token(key='284948256-otEee3ForNYRpOwUEV4y47gDHl7C15511KwmoiyT', secret='ZxedSOce174bfeW1r7zgbxuoXwbI7140YDXIKztitY')
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

# You MUST modify your username and password here ##############################################
			send_fanfou_msgs(text)
			ret = send_digu_msgs("yangchao.cs@gmail.com","19870810",text)
			msg=TweetID()
			msg.id=id
			msg.put()
# You MUST modify your twitter username  here ##################################################
#get the since_id
latest=getLatest()

getTweets(twitter_id="beyondchaos",since_id=latest)
