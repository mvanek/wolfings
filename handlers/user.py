import webapp2
import urllib
import json

from models import User


__all__ = ['UserHandler', 'UserIDHandler']


class UserHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler: /api/coupon
    '''
    def get(self):
        '''
        HTTP GET Method Handler
        Returns a list of user URI's
        '''
        self.response.status = '200 OK'
        for user in User.list_users(keys_only=True):
            self.response.write(user.id())

    def post(self):
        '''
        HTTP POST Method Handler
        Creates new user
        '''
        name = urllib.unquote(self.request.get('name'))
        user = User(name=name)
        key = user.put()
        self.response.status = '200 OK'
        self.response.write('/api/user/' + key.id())


class UserIDHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler: /api/coupon/[id]
    '''
    def get_id(self):
        return int(urllib.unquote(self.request.path.split('/')[3]))

    def get(self):
        '''
        HTTP GET Method Handler
        Returns JSON representation of coupon
        '''
        user = User.get_by_id(self.get_id())
        self.response.status = '200 OK'
        self.response.write(user.to_json())

    def put(self):
        '''
        HTTP PUT Method Handler
        Creates new user at the requested URI
        '''
        data = json.loads(self.request.body)
        user = User.get_by_id(self.get_id())
        for key, value in data.iteritems():
            setattr(user, key, value)
        key = user.put()
        self.response.status = '200 OK'
        self.response.write('/api/user/' + key.id())

    def delete(self):
        '''
        HTTP DELETE Method Handler
        Deletes exiting user
        '''
        user = User.get_by_id(self.get_id())
        user.key.delete()
        self.response.status = '204 No Content'
