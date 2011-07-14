from google.appengine.ext import webapp
from google.appengine.api import xmpp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext.webapp.template import render
from BeautifulSoup import BeautifulSoup
import urllib
import re
from os import path

class MainHandler(webapp.RequestHandler):
    def get(self):
		tmpl = path.join(path.dirname(__file__), "api.html")
		content = {}
		self.response.out.write(render(tmpl, content))

def main():
    application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
