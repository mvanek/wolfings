import webapp2
from RequestHandler import *
import urllib
import jinja2
import os
import datetime
from models import User
from google.appengine.api import users
from google.appengine.ext import ndb
import logging


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
        user_list = [u.dict() for u in
                 query.fetch_page(20, projection=(User.email,))[0]]
        logging.info(user_list)
        self.render(
            user_list=user_list
        )


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
        logging.info(u.held_coupons)
        logging.info(coupons)
        self.render(
            u=u,
            coupons=coupons
        )


class UserIDAdminHandler(RequestHandler):
    '''
    HTTP Request Handler, Entity: /user/[id]/edit
    '''
    def __init__(self, *args, **kwargs):
        super(UserIDHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('user_edit.jinja')
        self.idtype = str

    def get(self):
        cur_u = users.get_current_user()
        uid = self.get_page_id
        if uid != cur_u.user_id():
            self.abort(401)
        self.render(
            u=u
        )