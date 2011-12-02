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

def send_sina_msgs(username,password,msg):
	auth=base64.b64encode(username+":"+password)
	auth='Basic '+auth
	msg=unescape(msg)
	form_fields = {
			"status": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://api.t.sina.com.cn/statuses/update.xml?source=App_Key",
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

def send_sina_web_msgs(username,password,msg):
        # send sina msgs. use sina username, password.
        # the msgs parameter is a message list, not a single string.       
        result = urlfetch.fetch(url="https://login.sina.com.cn/sso/login.php?username=%s&password=%s&returntype=TEXT"%(username,password))
        cookie = Cookie.SimpleCookie(result.headers.get('set-cookie', ''))
        msg=unescape(msg)
        form_fields = {
          "content": msg,          
        }
        form_data = urllib.urlencode(form_fields)

        result = urlfetch.fetch(url="http://t.sina.com.cn/mblog/publish.php",
                            payload=form_data,
                            method=urlfetch.POST,
                            headers={'Referer':'http://t.sina.com.cn','Cookie' : make_cookie_header(cookie)})
        #print ""
        #print result.content
        
def send_163_msgs(username,password,msg):
        # send sina msgs. use sina username, password.
        # the msgs parameter is a message list, not a single string.       
        result = urlfetch.fetch(url="https://reg.163.com/logins.jsp?username=%s&password=%s&product=t&type=1"%(username,password))
        cookie = Cookie.SimpleCookie(result.headers.get('set-cookie', ''))
        msg=unescape(msg)
        form_fields = {
          "status": msg,          
        }
        form_data = urllib.urlencode(form_fields)

        result = urlfetch.fetch(url="http://t.163.com/statuses/update.do",
                            payload=form_data,
                            method=urlfetch.POST,
                            headers={'Referer':'http://t.163.com','Cookie' : make_cookie_header(cookie)})
        #print ""
        #print result.content
        
def send_sohu_msgs(username,password,msg):
	auth=base64.b64encode(username+":"+password)
	auth='Basic '+auth
	msg=unescape(msg)
	form_fields = {
			"status": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://api.t.sohu.com/statuses/update.xml",
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

def send_fanfou_msgs(username,password,msg):
	auth=base64.b64encode(username+":"+password)
	auth='Basic '+auth
	msg=unescape(msg)
	form_fields = {
			"status": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://api.fanfou.com/statuses/update.xml",
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
    
def send_9911_msgs(username,password,msg):
	auth=base64.b64encode(username+":"+password)
	auth='Basic '+auth
	msg=unescape(msg)
	form_fields = {
			"status": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://api.9911.com/statuses/update.xml",
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

def send_zuosa_msgs(username,password,msg):
	auth=base64.b64encode(username+":"+password)
	auth='Basic '+auth
	msg=unescape(msg)
	form_fields = {
			"status": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://api.zuosa.com/statuses/update.xml",
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

def send_renjian_msgs(username,password,msg):
	auth=base64.b64encode(username+":"+password)
	auth='Basic '+auth
	msg=unescape(msg)
	form_fields = {
			"text": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://api.renjian.com/statuses/update.xml",
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

def send_follow5_msgs(username,password,msg):
	auth=base64.b64encode(username+":"+password)
	auth='Basic '+auth
	msg=unescape(msg)
	form_fields = {
			"status": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://api.follow5.com/api/statuses/update.xml?api_key=9E76EE7693D280446FB6CA4A30754ED8",
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

def send_pingfm_msgs(api_key,user_app_key,msg):
	msg=unescape(msg)
	form_fields = {
			"api_key": api_key,
			"user_app_key": user_app_key,
			"post_method": "default",
			"body": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://api.ping.fm/v1/user.post",
			payload=form_data,
			method=urlfetch.POST
			)
	if result.status_code == 200:
		bk=result.content
		if bk.find("true"):
			return True
	else:
		return False

def send_hellotxt_msgs(user_key,app_key,msg):
	msg=unescape(msg)
	form_fields = {
			"user_key": user_key,
			"app_key": app_key,
			"body": msg,
			}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://hellotxt.com/api/v1/method/user.post",
			payload=form_data,
			method=urlfetch.POST
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
			#ret = send_sina_msgs("username@sina.com","password",text)
			ret = send_digu_msgs("username","password",text)
			ret = send_fanfou_msgs("username","password",text)
			#ret = send_163_msgs("username@163.com","password",text)
			#ret = send_sohu_msgs("username@sohu.com","password",text)
			#ret = send_9911_msgs("username","password",text)
			#ret = send_zuosa_msgs("username","password",text)
			#ret = send_renjian_msgs("username","password",text)
			#ret = send_follow5_msgs("username","password",text)
			#ret = send_pingfm_msgs("api_key","user_app_key",text)
			#ret = send_hellotxt_msgs("user_key","app_key",text)
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
parseTwitter(twitter_id="beyondchaos",since_id=latest)
