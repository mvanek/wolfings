#!/usr/bin/env python

import webapp2
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb


class Business(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPt()
    owners = ndb.UserProperty(repeated=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class LocationHandler(webapp2.RequestHandler):
    def get(self):
        zip_code = cgi.escape(self.request.get('zip'))


class BusinessHandler(webapp2.RequestHandler):
    def get(self):
        business_id = cgi.escape(self.request.get('id'))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return


def main():
    webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/api/location/', LocationHandler)
        ('/api/business/', BusinessHandler)
    ], debug=True)


if __name__ == '__main__':
    main()
