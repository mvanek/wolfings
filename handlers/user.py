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
           'UserIDHandler',
           'UserIDAdminHandler']


class BaseUserHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseUserHandler, self).__init__(*args, **kwargs)
        self.idtype = str
        cur_u = users.get_current_user()
        ukey = self.get_page_key()
        if not users.is_current_user_admin():
            if ukey.id() != cur_u.user_id():
                logging.info('Unauthorized user {} tried to access preference panel for user {}.'.format(cur_u.user_id(), ukey.id()))
                self.abort(401)


class UserHandler(BaseUserHandler):
    '''
    HTTP Request Handler, Collection: /user/
    '''
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('user_list.jinja')

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


class UserIDHandler(BaseUserHandler):
    '''
    HTTP Request Handler, Entity: /user/[id]
    '''
    def __init__(self, *args, **kwargs):
        super(UserIDHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('user.jinja')

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


class UserIDAdminHandler(BaseUserHandler):
    '''
    HTTP Request Handler, Entity: /user/[id]/edit
    '''
    def __init__(self, *args, **kwargs):
        super(UserIDAdminHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('user_edit.jinja')

    def get(self):
        self.render(
            u=self.get_page_entity()
        )

    def post(self):
        self.load_http_params({
            'surname': (str, False),
            'familiar_name': (str, False)
        })
        u = self.get_page_entity()
        try:
            if not self.params['surname']:
                self.render(
                    u=u,
                    status='Invalid surname.',
                    statusClass='failure'
                )
                return
        except KeyError:
            pass
        for k,v in self.params.iteritems():
            setattr(u,k,v)
        u.put()
        self.render(
            u=u,
            status='Successfully updated preferences.',
            statusClass='success'
        )