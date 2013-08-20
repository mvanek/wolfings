import webapp2
import urllib
import json

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
        business_id = int(urllib.unquote(self.request.get('business')))
        user_id = int(urllib.unquote(self.request.get('user')))
        active = bool(urllib.unquote(self.request.get('user')))
        self.status = '200 OK'
        for c in Coupon.list_coupons(user_id=user_id,
                                     business_id=business_id,
                                     active=active):
            self.response.write(c.id() + '\n')

    def post(self):
        '''
        HTTP POST Method Handler
        Creates new coupon
        '''
        name = urllib.unquote(self.request.get('name'))
        business = urllib.unquote(self.request.get('business'))
        coupon = Coupon.new(name=name, business=business)
        key = coupon.put()
        self.status = '200 OK'
        self.response.write('/api/coupon/' + key.id())


class CouponIDHandler(webapp2.RequestHandler):
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
        id = self.get_id()
        self.status = '200 OK'
        self.response.write(Coupon.get_by_id(id).to_json())

    def put(self):
        '''
        HTTP PUT Method Handler
        Creates new coupon at the requested URI
        '''
        coupon = Coupon.get_by_id(self.get_id())
        data = json.loads(self.request.body)
        for key, value in data.iteritems():
            setattr(coupon, key, value)
        key = coupon.put()
        self.status = '200 OK'
        self.response.write('/api/coupon/' + key.id())

    def delete(self):
        '''
        HTTP DELETE Method Handler
        Deletes exiting coupon
        '''
        coupon = Coupon.get_by_id(self.get_id())
        coupon.key.delete()
        self.status = '204 No Content'
