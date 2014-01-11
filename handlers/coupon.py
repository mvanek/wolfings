import webapp2
from RequestHandler import RequestHandler
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import ndb
import urllib
import jinja2
import os
import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
import dateutil.parser
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
        self.COUPONS_PER_PAGE = 5

    def get(self):
        '''
        Lists coupons, filtered by optional parameters
        Parameters: none
        '''
        page_number = int(self.request.GET.get('p', 1))
        qry = Coupon.query().order(Coupon.end)
        coupons = qry.fetch(
            limit=self.COUPONS_PER_PAGE,
            offset=((page_number - 1) * self.COUPONS_PER_PAGE)
        )

        self.response.write(self.template.render(
            coupons=coupons,
            page_number=page_number,
            total_pages=qry.count()/self.COUPONS_PER_PAGE
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
        self.response.write(self.template.render(
            c=c,
            b=b
        ))

    def post(self):
        c = self.get_page_entity()
        b = c.business.get()
        if not is_admin(b):
            self.abort(401)

        if self.request.POST.get('action') == 'update':
            self.load_http_params({
                'name': (str, True),
                'description': (str, True),
                'start_time': (str, True),
                'end_time': (str, True)
            })
            start = dateutil.parser.parse(self.params['start_time'], ignoretz=True)
            end = dateutil.parser.parse(self.params['end_time'], ignoretz=True)
            c.name          = self.params['name']
            c.description   = self.params['description']
            c.start         = start
            c.end           = end
        elif self.request.POST.get('action') == 'discontinue':
            c.visible = False
        c.put()
        self.redirect('/coupon/{}/'.format(c.key.id()))
