#!/usr/bin/env python


import wsgiref.handlers


from xml.dom import minidom
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import datetime
import time
import string

def get_text(nodelist):
  rc = ""
  for node in nodelist:
    if node.nodeType == node.TEXT_NODE:
      rc = rc + node.data
  return rc

username = 'williamlong'
#Output the html ick, but it's just a example
output = '<rss version="2.0">'
output += '<channel>'

# Make the API call to twitter
url = 'http://twitter.com/statuses/user_timeline/' + username + '.rss'
result = urlfetch.fetch(url)

#Status code ok?

if result.status_code == 200:
  file_xml = minidom.parseString(result.content)
  output += '<title>' + get_text(file_xml.getElementsByTagName("title")[0].childNodes) + '</title>'
  output += '<link>' + get_text(file_xml.getElementsByTagName("link")[0].childNodes) + '</link>'
  output += '<description>' + get_text(file_xml.getElementsByTagName("description")[0].childNodes) + '</description>'
  output += '<language>' + get_text(file_xml.getElementsByTagName("language")[0].childNodes) + '</language>'
  output += '<ttl>' + get_text(file_xml.getElementsByTagName("ttl")[0].childNodes) + '</ttl>'
  #Loop through the trends list
  items = file_xml.getElementsByTagName('item')
  for item in items:
    title = get_text(item.getElementsByTagName('title')[0].childNodes)
    if title.find('@',1) == -1 :
      output += '<item>'
      output += '<title>' + title.replace(username + ': ','') + '</title>'
      output += '<description>' + title.replace(username + ': ','') + '</description>'
      output += '<pubDate>' + get_text(item.getElementsByTagName('pubDate')[0].childNodes) + '</pubDate>'
      output += '<guid>' + get_text(item.getElementsByTagName('guid')[0].childNodes) + '</guid>'
      output += '<link>' + get_text(item.getElementsByTagName('link')[0].childNodes) + '</link>'
      output += '</item>'
  #Finish out the request
  output += '</channel>'
  output += '</rss>'
else:
  print "get twitter data error. "
  print result.content

#The primary handler, just outputs output
class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write(output)

#______________________________________________________________________________
def main():
  application = webapp.WSGIApplication([('/feed.*', MainHandler)],debug=True)
  wsgiref.handlers.CGIHandler().run(application)
if __name__ == '__main__':
  main()