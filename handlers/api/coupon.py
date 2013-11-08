import webapp2
from APIHandler import APIHandler
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Coupon
import json
import datetime


__all__ = ['CouponHandler', 'CouponIDHandler']


def str_to_datetime(s):
    return datetime.datetime.strptime(s.replace('Z', '000'),
                                      '%Y-%m-%dT%H:%M:%S.%f')


def authenticate(b=None):
    if users.is_current_user_admin():
        return True
    if b and ndb.Key('User', users.get_current_user().user_id()) in b.admins:
        return True
    webapp2.abort(401)


class CouponHandler(APIHandler):
    '''
    HTTP Request Handler: /api/coupon
    '''
    def __init__(self, *args, **kwargs):
        super(CouponHandler, self).__init__(Coupon, *args, **kwargs)

    def get(self):
        '''
        HTTP GET Method Handler
        Returns a JSON list of objects with keys 'name' and 'id'
        Parameters:
            - int business: the ID of the business that created the coupon
            - int user: the ID of the user whose coupons you want to check
            - int active: 0 if you want non-active coupons
        '''
        params = self.load_http_params({
            'business': (int, False),
            'user': (int, False),
            'year': (int, False),
            'month': (int, False),
            'day': (int, False),
            'hour': (int, False),
            'min': (int, False)
        }, use_default=True)
        try:
            time = datetime.datetime(
                params['year'],
                params['month'],
                params['day'],
                params['hour'],
                params['minute']
            )
        except KeyError:
            time = None

        coupon_keys = Coupon.list_coupons(
            user_id=params['user'],
            business_id=params['business'],
            time=time,
            keys_only=True
        )

        self.status = '200 OK'
        flag = False
        for key in coupon_keys:
            if flag:
                self.response.write('\n')
            else:
                flag = True
            self.response.write(str(key.id()) + '\n')

    def post(self):
        '''
        HTTP POST Method Handler
        Creates new coupon
        '''
        params = self.load_json_params({
            'business': (int, True),
            'name': (str, True),
            'start': (str_to_datetime, True),
            'end': (str_to_datetime, True)
        })
        business_key = ndb.Key('Business', params['business'])
        authenticate(business_key.get())
        key = Coupon(
            name=params['name'],
            business=business_key,
            start=params['start'],
            end=params['end']
        ).put()
        self.status = '200 OK'
        self.response.write('/api/coupon/' + str(key.id()))


class CouponIDHandler(APIHandler):
    '''
    HTTP Request Handler: /api/coupon/[id]
    '''
    def __init__(self, *args, **kwargs):
        super(CouponIDHandler, self).__init__(Coupon, *args, **kwargs)

    def get(self):
        '''
        HTTP GET Method Handler
        Returns JSON representation of coupon
        '''
        self.status = '200 OK'
        self.response.write(self.get_entity().json())

    def put(self):
        '''
        HTTP PUT Method Handler
        Creates new coupon at the requested URI
        '''
        coupon = self.get_entity()
        authenticate(coupon.business.get())
        params = self.load_json_params({
            'business': (int, False),
            'name': (str, False),
            'start': (str_to_datetime, False),
            'end': (str_to_datetime, False)
        })
        for key, value in params.iteritems():
            if key == 'business':
                value = ndb.Key('Business', value)
            setattr(coupon, key, value)
        key = coupon.put()
        self.status = '200 OK'
        self.response.write('/api/coupon/' + str(key.id()))

    def delete(self):
        '''
        HTTP DELETE Method Handler
        Deletes exiting coupon
        '''
        coupon = self.get_entity()
        authenticate(coupon.business.get())
        coupon.key.delete()
        self.status = '204 No Content'
