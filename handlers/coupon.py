import webapp2
from RequestHandler import RequestHandler
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import ndb
import urllib
import jinja2
import os
import datetime
import logging
from models import Business, Coupon, User


__all__ = ['CouponHandler',
           'CouponIDHandler',
           'CouponIDEditHandler']


def is_admin(b=None):
    if users.is_current_user_admin():
        return True
    if b:
        return ndb.Key('User', users.get_current_user().user_id()) in b.admins
    return False


def collection_callback(business):
    return Coupon.get_by_business(business.key.id())


class CouponHandler(RequestHandler):
    '''
    HTTP Request Handler, Collection: /coupon/
    '''
    def __init__(self, *args, **kwargs):
        super(CouponHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('coupon_list.jinja')
        self.idtype = int

    def get(self):
        '''
        Lists coupons, filtered by optional parameters
        Parameters:
            name - Name of the business
            lat,lon - Location of the business
        '''
        try:
            lat = float(urllib.unquote(self.request.get('lat')))
            lon = float(urllib.unquote(self.request.get('lon')))
        except ValueError:
            query = Business.query()
        else:
            query = Business.query_location(lat=lat, lon=lon)

        name = urllib.unquote(self.request.get('name'))
        if name:
            query = query.filter(Business.name == name)
        coupons = [c for business in query.map(lambda x: Coupon.get_by_business(x.key.id()))
                   for c in business]
        coupons = sorted(coupons, lambda x, y: cmp(x.end, y.end))
        now = datetime.datetime.now()
        i = 0
        expired_index = None

        for i in range(len(coupons)):
            if expired_index is None and now < coupons[i].end:
                expired_index = i
            if now < coupons[i].start:
                break
        expired = coupons[0:expired_index]
        active = coupons[expired_index:i]
        inactive = coupons[i:]

        self.response.status = '200 OK'
        self.response.write(self.template.render(
            coupons=active+inactive+expired
        ))


class CouponIDHandler(RequestHandler):
    '''
    HTTP Request Handler, Entity: /coupon/[id]/
    '''
    def __init__(self, *args, **kwargs):
        super(CouponIDHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('coupon.jinja')
        self.idtype = int

    def get(self):
        '''
        Returns business entity
        '''
        c = self.get_page_entity()
        b = c.business.get()
        self.response.status = '200 OK'
        self.response.write(self.template.render(
            c=c,
            b=b
        ))


class CouponIDEditHandler(RequestHandler):
    '''
    HTTP Request Handler, Entity: /coupon/[id]/admin/
    '''
    def __init__(self, *args, **kwargs):
        super(CouponIDEditHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('coupon_edit.jinja')
        self.idtype = int

    def get(self):
        c = self.get_page_entity()
        b = c.business.get()
        if not is_admin(b):
            self.abort(401)
        self.response.status = '200 OK'
        self.response.write(self.template.render(
            c=c,
            b=b
        ))
