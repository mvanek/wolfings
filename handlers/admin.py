import jinja2
import os
import webapp2
from RequestHandler import *
from google.appengine.api import users
from google.appengine.ext import ndb
from models import User, Business
import logging


__all__ = ['AdminHandler', 'OldAdminHandler']


class AdminHandler(RequestHandler):
    '''
    HTTP Request Handler: /admin/
    '''
    def __init__(self, *args, **kwargs):
        super(AdminHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('admin.jinja')

    def get(self):
        '''
        HTTP GET Method Handler
        Parameters: None
        '''
        if not users.is_current_user_admin():
            self.abort(404)
        qry = User.query(projection=[User.email]).order(User.email)
        self.response.write(self.template.render(
            user_iter=qry.iter()
        ))

    def post(self):
        '''
        HTTP POST Method Handler
        Parameters: None
        '''
        if not users.is_current_user_admin():
            self.abort(404)
        self.load_http_params({
            'name': (str, True),
            'adm': (lambda s: ndb.Key(urlsafe=s), True),
            'lat': (float, True),
            'lon': (float, True)
        })
        b = Business(
            name=self.params['name'],
            lat=self.params['lat'],
            lon=self.params['lon'],
            admins=[self.params['adm']]
        )
        b.put()
        qry = User.query(projection=[User.email]).order(User.email)
        self.render(
            user_iter=qry.iter(),
            statusClass='success',
            status='Succesfully created business "<a href="/business/{}/">{}</a>"'.format(b.key.id(), b.name)
        )


class OldAdminHandler(RequestHandler):
    '''
    HTTP Request Handler: /admin/old/
    '''
    def __init__(self, *args, **kwargs):
        super(OldAdminHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('oldadmin.jinja')

    def get(self):
        '''
        HTTP GET Method Handler
        Parameters: None
        '''
        if not users.is_current_user_admin():
            self.abort(404)
        self.response.write(self.template.render())
