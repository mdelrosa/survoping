# guestbook.py

import os
import cgi
import urllib
import urllib2
import json

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

DEFAULT_GUESTBOOK_NAME = "default_guestbook"

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
		return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):

	def get(self):
		template_values = {
			'values?': "don't need em"
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

class Ping(webapp2.RequestHandler):

	def get(self):
		url = 'http://survo.herokuapp.com/mail/decklist'
		res = urllib2.urlopen(url)
		response = json.loads(res.read())

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/ping', Ping)
], debug=True)