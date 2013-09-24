from google.appengine.ext import ndb
import webapp2
import urllib
import json
import datetime

from models import Coupon


__all__ = ['CouponHandler', 'CouponIDHandler']


class CouponHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler: /api/coupon
    '''
    def get(self):
        '''
        HTTP GET Method Handler
        Returns a JSON list of objects with keys 'name' and 'id'
        Parameters:
            - int business: the ID of the business that created the coupon
            - int user: the ID of the user whose coupons you want to check
            - int active: 0 if you want non-active coupons
        '''
        try:
            business_id = int(urllib.unquote(self.request.get('business')))
        except ValueError:
            business_id = None
        try:
            user_id = int(urllib.unquote(self.request.get('user')))
        except ValueError:
            user_id = None
        try:
            month = int(urllib.unquote(self.request.get('month')))
            day = int(urllib.unquote(self.request.get('day')))
            year = int(urllib.unquote(self.request.get('year')))
            hour = int(urllib.unquote(self.request.get('hour')))
            minute = int(urllib.unquote(self.request.get('min')))
            time = datetime.datetime(year, month, day, hour, minute)
        except ValueError:
            time = None
        self.status = '200 OK'
        for key in Coupon.list_coupons(user_id=user_id,
                                       business_id=business_id,
                                       time=time,
                                       keys_only=True):
            self.response.write(str(key.id()) + '\n')

    def post(self):
        '''
        HTTP POST Method Handler
        Creates new coupon
        '''
        name = urllib.unquote(self.request.get('name'))
        business = urllib.unquote(self.request.get('business'))
        coupon = Coupon(name=name, business=business)
        key = coupon.put()
        self.status = '200 OK'
        self.response.write('/api/coupon/' + key.id())


class CouponIDHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler: /api/coupon/[id]
    '''
    def get_id(self):
        return int(urllib.unquote(self.request.path.split('/')[3]))

    def get_coupon(self):
        c = Coupon.get_by_id(self.get_id())
        if c:
            return c
        self.abort(404)

    def get(self):
        '''
        HTTP GET Method Handler
        Returns JSON representation of coupon
        '''
        self.status = '200 OK'
        self.response.write(self.get_coupon().to_json())

    def put(self):
        '''
        HTTP PUT Method Handler
        Creates new coupon at the requested URI
        '''
        coupon = self.get_coupon()
        data = json.loads(self.request.body)
        try:
            data['business'] = ndb.Key('Business', int(data['business']))
        except ValueError:
            self.abort(400)
        except KeyError:
            pass
        for key, value in data.iteritems():
            setattr(coupon, key, value)
        key = coupon.put()
        self.status = '200 OK'
        self.response.write('/api/coupon/' + str(key.id()))

    def delete(self):
        '''
        HTTP DELETE Method Handler
        Deletes exiting coupon
        '''
        coupon = self.get_coupon()
        coupon.key.delete()
        self.status = '204 No Content'
