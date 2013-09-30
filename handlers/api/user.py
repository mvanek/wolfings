import webapp2
import urllib
import json

from google.appengine.ext import ndb
from models import User, Coupon


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
        for key in User.list_users(keys_only=True):
            self.response.write(str(key.id()) + '\n')

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
        try:
            data['held_coupons'] = [ndb.Key('Coupon', i) for i in
                                    data['held_coupons']]
        except KeyError:
            pass
        user = User.get_by_id(self.get_id())
        for key, value in data.iteritems():
            setattr(user, key, value)
        key = user.put()
        self.response.status = '200 OK'
        self.response.write('/api/user/' + str(key.id()))

    def delete(self):
        '''
        HTTP DELETE Method Handler
        Deletes exiting user
        '''
        user = User.get_by_id(self.get_id())
        user.key.delete()
        self.response.status = '204 No Content'


class UserIDCouponHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler: /api/user/[id]/coupons/
    '''
    def get_uid(self):
        try:
            return int(urllib.unquote(self.request.path.split('/')[3]))
        except ValueError:
            self.abort(404)

    def get_cid(self):
        try:
            return int(urllib.unquote(self.request.get('coupon')))
        except ValueError:
            self.abort(400)

    def post(self):
        '''
        HTTP GET Method Handler
        Returns JSON representation of coupon
        '''
        coupon = Coupon.get_by_id(self.get_cid())
        if not coupon:
            self.abort(400)
        user = User.get_by_id(self.get_uid())
        if not user:
            self.abort(400)
        if coupon.key not in user.held_coupons:
            user.held_coupons.append(coupon.key)
            user.put()
        self.response.status = '200 OK'
        self.response.write('/api/user/' + str(user.key.id()))
