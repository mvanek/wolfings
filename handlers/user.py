import webapp2
import urllib
import jinja2
import os
import datetime
from models import User


__all__ = ['UserHandler',
           'UserIDHandler']


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    trim_blocks=True)


def get_id(request):
    return int(urllib.unquote(request.path.split('/')[2]))


def get_user(request):
    '''
    Returns user entity, and aborts with code 404 if there's no entity
    '''
    u = User.get_by_id(get_id(request))
    if u:
        return u
    webapp2.abort(404)


class UserHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Collection: /user/
    '''
    def get(self):
        '''
        Lists useres, filtered by optional parameters
        Parameters:
            name - Name of the user
            lat,lon - Location of the user
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
    HTTP Request Handler, Entity: /user/[id]
    '''
    def get(self):
        '''
        Returns user entity
        '''
        u = get_user(self.request)
        coupons = [key.get() for key in u.held_coupons]
        template = JINJA_ENVIRONMENT.get_template('user.jinja')
        self.response.status = '200 OK'
        self.response.write(template.render(name=u.name,
                                            coupons=coupons,
                                            now=datetime.datetime.now(),
                                            user=User.query(User.name == 'Dick').get()))
