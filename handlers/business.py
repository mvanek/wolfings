import webapp2
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.api import images
import urllib
import jinja2
import os
import datetime
from models import Business, Coupon, User


__all__ = ['BusinessHandler',
           'BusinessIDHandler',
           'BusinessIDAdminHandler',
           'BusinessIDAdminCouponHandler',
           'BusinessIDUploadHandler']


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    trim_blocks=True)


def get_id(request):
    return int(urllib.unquote(request.path.split('/')[2]))


def get_business(request):
    '''
    Returns business entity, and aborts with code 404 if there's no entity
    '''
    b = Business.get_by_id(get_id(request))
    if b:
        return b
    webapp2.abort(404)


class BusinessHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Collection: /business
    '''
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

        template = JINJA_ENVIRONMENT.get_template('business_list.jinja')
        self.response.status = '200 OK'
        self.response.write(template.render(businesses=businesses,
                                            user=User.query(User.name == 'Dick').get()))


class BusinessIDHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Entity: /business/[id]
    '''
    def get(self):
        '''
        Returns business entity
        '''
        b = get_business(self.request)
        coupons = Coupon.get_by_business(b.key.id())

        template = JINJA_ENVIRONMENT.get_template('business.jinja')
        self.response.status = '200 OK'
        self.response.write(template.render(b=b,
                                            coupons=coupons,
                                            now=datetime.datetime.now(),
                                            user=User.query(User.name == 'Dick').get()))


class BusinessIDAdminHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Entity: /business/[id]/admin
    '''
    def get(self):
        mark_upload = blobstore.create_upload_url('/business/{}/upload/'
                                                  .format(get_id(self.request)))
        b = get_business(self.request)

        template = JINJA_ENVIRONMENT.get_template('business_admin.jinja')
        self.response.status = '200 OK'
        self.response.write(template.render(name=b.name,
                                            mark_upload=mark_upload,
                                            user=User.query(User.name == 'Dick').get()))


class BusinessIDAdminCouponHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Entity: /business/[id]/admin
    '''
    def get(self):
        b = get_business(self.request)
        coupons = Coupon.get_by_business(get_id(self.request))

        template = JINJA_ENVIRONMENT.get_template('business_admin_coupon.jinja')
        self.response.status = '200 OK'
        self.response.write(template.render(b=b,
                                            coupons=coupons,
                                            now=datetime.datetime.now(),
                                            user=User.query(User.name == 'Dick').get()))


class BusinessIDUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    '''
    HTTP Request Handler, Entity: /business/[id]/upload
    '''
    def post(self):
        blob_info = self.get_uploads('mark')[0]
        b = get_business(self.request)
        b.mark = blob_info.key()
        b.put()

        self.redirect('/business/{}/admin/'.format(get_id(self.request)))
