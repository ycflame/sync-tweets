#!/usr/bin/env python
import oauth2 as oauth
import urllib

# Create your consumer with the proper key/secret.
consumer = oauth.Consumer(key="52b62bd6315d823a32bcfe4dfaa40119", secret="62189cb88e31febd707cb8337231e18a")
token = oauth.Token(key="your_access_token", secret="your_access_secret")

# Request token URL for Twitter.
#request_token_url = "http://api.fanfou.com/account/notification.json"

post_url = "http://api.fanfou.com/statuses/update.json"

# Create our client.
client = oauth.Client(consumer, token)

# The OAuth Client request works just like httplib2 for the most part.
body = { 
		"status": 'I love fanfou',
		}
form_data = urllib.urlencode(body)

resp, content = client.request(post_url, "POST", form_data)
print resp
print content
