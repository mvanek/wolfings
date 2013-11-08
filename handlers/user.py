import webapp2
from RequestHandler import *
import urllib
import jinja2
import os
import datetime
from models import User
from google.appengine.api import users
from google.appengine.ext import ndb


__all__ = ['UserHandler',
           'UserIDHandler']


class UserHandler(RequestHandler):
    '''
    HTTP Request Handler, Collection: /user/
    '''
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('user_list.jinja')
        self.idtype = str

    def get(self):
        '''
        Lists useres, filtered by optional parameters
        Parameters:
            name - Name of the user
            lat,lon - Location of the user
        '''
        query = User.query()
        users = [u.dict() for u in
                 query.fetch_page(20, projection=[User.name])[0]]
        self.response.status = '200 OK'
        self.response.write(self.template.render(
            users=users
        ))


class UserIDHandler(RequestHandler):
    '''
    HTTP Request Handler, Entity: /user/[id]
    '''
    def __init__(self, *args, **kwargs):
        super(UserIDHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('user.jinja')
        self.idtype = str

    def get(self):
        '''
        Returns user entity
        '''
        u = self.get_page_entity()
        coupons = ndb.get_multi(u.held_coupons)
        self.response.status = '200 OK'
        self.response.write(self.template.render(
            u=u,
            coupons=coupons
        ))
