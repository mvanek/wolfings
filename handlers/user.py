import webapp2
import urllib
import jinja2
import os
import datetime
from models import User


__all__ = ['UserHandler',
           'UserIDHandler',
           'UserIDAdminHandler']


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    trim_blocks=True)


class UserHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Collection: /business
    '''
    def get(self):
        '''
        Lists businesses, filtered by optional parameters
        Parameters:
            name - Name of the business
            lat,lon - Location of the business
        '''
        query = User.query()

        template = JINJA_ENVIRONMENT.get_template('user_list.jinja')
        users = [u.dict() for u in
                 query.fetch_page(20, projection=[User.name])[0]]
        self.response.status = '200 OK'
        self.response.write(template.render(users=users,
                                            user=User.query(User.name == 'Dick').get()))


class UserIDHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Entity: /business/[id]
    '''
    def get_id(self):
        return int(urllib.unquote(self.request.path.split('/')[2]))

    def get_user(self):
        '''
        Returns business entity, and aborts with code 404 if there's no entity
        '''
        u = User.get_by_id(self.get_id())
        if u:
            return u
        self.abort(404)

    def get(self):
        '''
        Returns business entity
        '''
        u = self.get_user()
        coupons = [key.get() for key in u.held_coupons]
        template = JINJA_ENVIRONMENT.get_template('user.jinja')
        self.response.status = '200 OK'
        self.response.write(template.render(name=u.name,
                                            coupons=coupons,
                                            now=datetime.datetime.now(),
                                            user=User.query(User.name == 'Dick').get()))


class UserIDAdminHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Entity: /business/[id]/admin
    '''
    def get_id(self):
        return int(urllib.unquote(self.request.path.split('/')[2]))

    def get_business(self):
        '''
        Returns business entity, and aborts with code 404 if there's no entity
        '''
        u = User.get_by_id(self.get_id())
        if u:
            return u
        self.abort(404)

    def get(self):
        u = self.get_business()
        template = JINJA_ENVIRONMENT.get_template('user_admin.jinja')
        self.response.status = '200 OK'
        self.response.write(template.render(name=u.name,
                                            user=User.query(User.name == 'Dick').get()))
