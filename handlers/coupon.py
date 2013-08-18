import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

import json
import urllib

import models


__all__ = ['CouponHandler']


def user_exists(user_id):
    '''
    Checks datastore for user
    '''
    query = models.User.get_by_id(user_id)
    return bool(query)


class CouponHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler: /api/coupon/[id]
    '''
    def get_id(self):
        '''
        Returns coupon ID
        '''
        if not self.coupon_id:
            self.coupon_id = urllib.unquote(self.request.path.split('/')[3])
        return self.coupon_id

    def get_coupon(self):
        '''
        Returns coupon entity
        '''
        if not self.coupon:
            self.coupon = models.Coupon.get_by_id(self.get_id())
        return self.coupon

    def get_business(self, business_id=None):
        '''
        Returns business entity
        '''
        if not self.business:
            if business_id:
                self.business = models.Business.get_by_id(business_id)
            else:
                self.business = self.get_coupon().business.get()
        return self.business

    def authenticate(self, business_id=None):
        '''
        Authenticates current user against business owners
        '''
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            self.abort()
        if users.is_current_user_admin():
            return True
        user_ids = [key.id() for key in self.get_business(business_id).owners]
        if user.user_id() in user_ids:
            return True
        self.abort(401)

    def get(self):
        '''
        HTTP GET Method Handler
        Returns JSON representation of coupon
        '''
        try:
            self.response.write(json.dumps(self.get_coupon().to_dict()))
        except AttributeError:
            self.abort(404)

    def post(self):
        '''
        HTTP POST Method Handler
        Updates existing coupon
        '''
        self.authenticate()

        name = urllib.unquote(self.request.get('name'))
        description = urllib.unquote(self.request.get('description'))
        if not (name or description):
            self.abort(400, 'Nothing changed')

        coupon = self.get_coupon()
        if not coupon:
            self.abort(404)
        if name:
            coupon.name = name
        if description:
            coupon.description = description

    def put(self):
        '''
        HTTP PUT Method Handler
        Creates a new coupon
        '''
        business_id = urllib.unquote(self.request.get('business'))
        business = models.Business.get_by_id(business_id)
        try:
            self.authenticate([key.id() for key in business.owners])
        except AttributeError:
            self.abort(400, 'Invalid business id')

        coupon = models.Coupon(
            id=self.get_id(),
            name=urllib.unquote(self.request.get('name')),
            business=business_id,
            description=urllib.unquote(self.request.get('description')))
        coupon.put()

    def delete(self):
        '''
        HTTP DELETE Method Handler
        Deletes exiting coupon
        '''
        business_id = urllib.unquote(self.request.get('business'))
        business = models.Business.get_by_id(business_id)
        try:
            self.authenticate([key.id() for key in business.owners])
        except AttributeError:
            self.abort(400, 'Invalid business id')
        ndb.Key('Coupon', self.get_id()).delete()
