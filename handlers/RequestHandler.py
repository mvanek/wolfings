import logging
import webapp2
import urllib
import jinja2
import os
import datetime
from models import User
from google.appengine.ext import ndb
from google.appengine.api import users


__all__ = ['RequestHandler',
           'get_cur_user']


def get_cur_user():
    user = users.get_current_user()
    if user:
        return User.get_by_id(user.user_id())
    return None

@jinja2.environmentfunction
def is_admin(env, b=None):
    if users.is_current_user_admin():
        return True
    if b and env.globals['user']:
        return env.globals['user'].key in b.admins
    return False

class RequestHandler(webapp2.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(RequestHandler, self).__init__(*args, **kwargs)
        self.JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.join(
                os.path.dirname(__file__),
                'templates'
            )),
            extensions=['jinja2.ext.autoescape'],
            trim_blocks=True
        )
        cur_user = get_cur_user()
        self.JINJA_ENVIRONMENT.globals['users'] = users
        self.JINJA_ENVIRONMENT.globals['user'] = get_cur_user()
        self.JINJA_ENVIRONMENT.globals['now'] = datetime.datetime.now()
        self.JINJA_ENVIRONMENT.globals['is_admin'] = is_admin

    def get_page_id(self):
        pathparts = urllib.unquote(self.request.path).split('/')
        return pathparts[2]

    def get_page_key(self):
        pathparts = urllib.unquote(self.request.path).split('/')
        path_len = len(pathparts)
        page_id = pathparts[2]
        page_modelname = pathparts[1].capitalize()
        key = ndb.Key(page_modelname, self.idtype(page_id))
        return key

    def get_page_entity(self):
        key = self.get_page_key()
        logging.info(key)
        entity = key.get()
        if not entity:
            self.abort(404)
        return entity
