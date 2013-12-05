import webapp2
from RequestHandler import RequestHandler, get_cur_user
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.api import users
import urllib
import jinja2
import os
import datetime
import logging
from models import Business, Coupon, User, Address


__all__ = ['BusinessHandler',
           'BusinessIDHandler',
           'BusinessIDAdminHandler',
           'BusinessIDManageHandler',
           'BusinessIDUploadHandler']


def is_admin(b=None):
    if users.is_current_user_admin():
        return True
    if b:
        return ndb.Key('User', users.get_current_user().user_id()) in b.admins
    return False


class BusinessHandler(RequestHandler):
    '''
    HTTP Request Handler, Page: /business/
    '''
    def __init__(self, *args, **kwargs):
        super(BusinessHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('business_list.jinja')
        self.idtype = int

    def get(self):
        '''
        Lists businesses, filtered by optional parameters
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
        businesses = query.fetch_page(20, projection=[Business.name])[0]
        self.response.status = '200 OK'
        self.response.write(self.template.render(
            businesses=businesses
        ))


class BusinessIDHandler(RequestHandler):
    '''
    HTTP Request Handler, Page: /business/[id]/
    '''
    def __init__(self, *args, **kwargs):
        super(BusinessIDHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('business.jinja')
        self.idtype = int

    def get(self):
        '''
        Returns business entity
        '''
        key = self.get_page_key()
        coupons = Coupon.get_by_business(key.id())

        i = 0
        expired_index = None
        now = datetime.datetime.now()
        coupons = sorted(coupons, lambda x, y: cmp(x.end, y.end))
        for i in range(len(coupons)):
            if expired_index is None and now < coupons[i].end:
                expired_index = i
            if now < coupons[i].start:
                break
        expired = coupons[0:expired_index]
        active = coupons[expired_index:i]
        inactive = coupons[i:]
        logging.info('expired')
        logging.info(expired)
        logging.info('active')
        logging.info(active)
        logging.info('inactive')
        logging.info(inactive)

        self.response.status = '200 OK'
        self.response.write(self.template.render(
            b=key.get(),
            coupons=active+inactive+expired
        ))


class BusinessIDAdminHandler(RequestHandler):
    '''
    HTTP Request Handler, Page: /business/[id]/admin/
    '''
    def __init__(self, *args, **kwargs):
        super(BusinessIDAdminHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('business_admin.jinja')
        self.idtype = int

    def get(self):
        key = self.get_page_key()
        b = key.get()
        if not is_admin(b):
            self.abort(401)
        admins = ndb.get_multi(b.admins)
        mark_upload = blobstore.create_upload_url(
                '/business/{}/upload/'.format(key.id())
        )
        self.response.status = '200 OK'
        self.response.write(self.template.render(
            b=b,
            admins=admins,
            mark_upload=mark_upload
        ))

    def post(self):
        self.load_http_params({
            'name': (str, True),
            'description': (str, True),
            'address': (str, True),
            'city': (str, True),
            'state': (str, True),
            'zip': (int, True)
        })
        key = self.get_page_key()
        b = key.get()
        if not is_admin(b):
            self.abort(401)
        address_parts    = self.params['address'].split(' ', 1)
        self.response.write(address_parts[0])
        b.name           = self.params['name']
        b.description    = self.params['description']
        b.address.number = int(address_parts[0])
        b.address.street = address_parts[1]
        b.address.city   = self.params['city']
        b.address.state  = self.params['state']
        b.address.zip    = self.params['zip']
        b.put()
        self.redirect('.')


class BusinessIDManageHandler(RequestHandler):
    '''
    HTTP Request Handler, Page: /business/[id]/manage/
    '''
    def __init__(self, *args, **kwargs):
        super(BusinessIDManageHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('business_verify.jinja')
        self.idtype = int

    def get(self):
        b = self.get_page_entity()
        if not is_admin(b):
            self.abort(401)
        coupons = Coupon.get_by_business(b.key.id())
        self.response.status = '200 OK'
        self.response.write(self.template.render(
            b=b,
            coupons=coupons
        ))


class BusinessIDUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    '''
    HTTP Request Handler, Page: /business/[id]/upload
    '''
    def post(self):
        blob_info = self.get_uploads('mark')[0]
        page_id = int(urllib.unquote(self.request.path).split('/')[2])
        key = ndb.Key('Business', page_id);
        b = key.get()
        if not is_admin(b):
            self.abort(401)
        b.mark = blob_info.key()
        b.put()
        self.redirect('/business/{}/admin/'.format(key.id()))
