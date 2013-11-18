import webapp2
import logging
import urllib
from APIHandler import APIHandler

from google.appengine.ext import ndb
from google.appengine.api import users
from models import Address, User, Coupon, Business


__all__ = ['UserHandler', 'UserIDHandler',
           'UserIDCouponHandler', 'UserIDCouponIDHandler']


def is_admin(uid=None, bid=None):
    if users.is_current_user_admin():
        return True
    cur_user = users.get_current_user().user_id()
    if uid == cur_user:
        return True
    if bid:
        user_key = ndb.Key('User', cur_user)
        admins = Business.get_by_id(bid).admins
        logging.info(user_key)
        logging.info(admins)
        return user_key in admins
    return False


def authenticate(uid=None, bid=None):
    if not is_admin(uid, bid):
        webapp2.abort(401)


class UserHandler(APIHandler):
    '''
    HTTP Request Handler: /api/user
    '''
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(User, *args, idtype=str, **kwargs)

    def get(self):
        '''
        HTTP GET Method Handler
        Returns a list of user URI's
        '''
        params = self.load_http_params({
            'name': (str, False),
            'email': (str, False),
            'phone': (str, False),
            'number': (str, False),
            'street': (str, False),
            'city': (str, False),
            'zip': (int, False),
            'country': (str, False)
        })
        param2prop = {
            'name': User.name,
            'email': User.email,
            'phone': User.phone,
            'number': User.address.number,
            'street': User.address.street,
            'city': User.address.city,
            'zip': User.address.zip,
            'country': User.address.country
        }
        q = User.query()
        for k,v in params.iteritems():
            q = q.filter(param2prop[k] == v)

        self.response.status = '200 OK'
        flag = False
        for key in q.iter(keys_only=True):
            if flag:
                self.response.write('\n')
            else:
                flag = True
            self.response.write(str(key.id()))

    def post(self):
        '''
        HTTP POST Method Handler
        Creates new user from JSON representation
        '''
        authenticate()
        key = User(**self.load_json_params({
            'name': (str, True),
            'email': (str, True),
            'phone': (str, False),
            'address': (lambda d: Address(**d), False),
            'held_coupons': (lambda l: [ndb.Key('Coupon', int(c)) for c in list(l)], False),
        })).put()
        self.response.status = '200 OK'
        self.response.write('/api/user/' + key.id())


class UserIDHandler(APIHandler):
    '''
    HTTP Request Handler: /api/user/[id]
    '''
    def __init__(self, *args, **kwargs):
        super(UserIDHandler, self).__init__(User, *args, idtype=str, **kwargs)

    def get(self):
        '''
        HTTP GET Method Handler
        Returns JSON representation of coupon
        '''
        user = User.get_by_id(self.get_id())
        self.response.status = '200 OK'
        self.response.write(user.json())

    def put(self):
        '''
        HTTP PUT Method Handler
        Creates new user at the requested URI
        '''
        uid = self.get_id()
        authenticate(uid)
        params = self.load_json_params({
            'name': (str, True),
            'email': (str, True),
            'phone': (str, False),
            'address': (lambda d: Address(**d), False),
            'held_coupons': (lambda l: [ndb.Key('Coupon', int(c)) for c in list(l)], False),
        })
        user = User.get_by_id(uid)
        for key, value in params.iteritems():
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
            return urllib.unquote(self.request.path.split('/')[3])
        except ValueError:
            self.abort(404)

    def get_bid(self):
        try:
            return int(urllib.unquote(self.request.get('business')))
        except ValueError:
            self.abort(400)

    def get_cid(self):
        try:
            return int(urllib.unquote(self.request.get('coupon')))
        except ValueError:
            self.abort(400)

    def get(self):
        '''
        HTTP POST Method Handler
        Searches user's coupons
        '''
        authenticate(self.get_uid(), self.get_bid())
        self.response.status = '200 OK'
        for k in Coupon.get_by_user_and_business(self.get_uid(),
                                                 self.get_bid(),
                                                 keys_only=True):
            self.response.write(str(k.id()) + '\n')

    def post(self):
        '''
        HTTP POST Method Handler
        Gives user a coupon
        '''
        authenticate(self.get_uid())
        user = User.get_by_id(self.get_uid())
        coupon = Coupon.get_by_id(self.get_cid())
        if not coupon:
            self.abort(400)
        if not user:
            self.abort(400)
        if coupon.key not in user.held_coupons:
            user.held_coupons.append(coupon.key)
            user.put()
        self.response.status = '200 OK'
        self.response.write('/api/user/' + str(user.key.id()))


class UserIDCouponIDHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler: /api/user/[id]/coupons/[id]
    '''
    def get_uid(self):
        try:
            return urllib.unquote(self.request.path.split('/')[3])
        except ValueError:
            self.abort(404)

    def get_cid(self):
        try:
            return int(urllib.unquote(self.request.path.split('/')[5]))
        except ValueError:
            self.abort(404)

    def delete(self):
        '''
        HTTP DELETE Method Handler
        Takes coupon away from user
        '''
        user = User.get_by_id(self.get_uid())
        if not user:
            self.abort(400)
        coupon_key = ndb.Key('Coupon', self.get_cid())
        authenticate(self.get_uid(), coupon_key.get().business.id())
        user.held_coupons.remove(coupon_key)
        user.put()
        self.response.status = '204 No Content'


class UserIDCouponIDHandler(APIHandler):
    '''
    HTTP Request Handler: /api/user/[id]/coupons/[id]
    '''
    def __init__(self, *args, **kwargs):
        super(UserIDCouponIDHandler, self).__init__(User, *args, idtype=str, **kwargs)

    def get_uid(self):
        try:
            return urllib.unquote(self.request.path.split('/')[3])
        except ValueError:
            self.abort(404)

    def get_cid(self):
        try:
            return int(urllib.unquote(self.request.path.split('/')[5]))
        except ValueError:
            self.abort(404)

    def post(self):
        '''
        HTTP POST Method Handler
        Verifies coupon
        '''
        params = self.load_http_params({
            'verify': (bool, True)
        })
        user = self.get_entity()
        coupon_key = ndb.Key('Coupon', self.get_cid())
        authenticate(bid=coupon_key.get().business.id())
        if coupon_key not in user.held_coupons:
            self.abort(404)
        if not params['verify']:
            self.abort(400)
        user.old_coupons.append(coupon_key)
        user.held_coupons.remove(coupon_key)
        user.put()
        self.response.status = '200 OK'
        self.response.write = '/api/user/{}/history/{}'.format(
            user.key.id(),
            coupon_key.id()
        )

    def delete(self):
        '''
        HTTP DELETE Method Handler
        Takes coupon away from user
        '''
        user = User.get_by_id(self.get_uid())
        if not user:
            self.abort(400)
        coupon_key = ndb.Key('Coupon', self.get_cid())
        authenticate(self.get_uid(), coupon_key.get().business.id())
        user.held_coupons.remove(coupon_key)
        user.put()
        self.response.status = '204 No Content'
