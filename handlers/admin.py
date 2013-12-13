import jinja2
import os
import webapp2
from RequestHandler import *
from google.appengine.api import users


__all__ = ['AdminHandler']

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'])


class AdminHandler(RequestHandler):
    '''
    HTTP Request Handler: /api/coupon
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
        self.response.write(self.template.render())
