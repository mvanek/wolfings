import webapp2
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.api import images
import urllib
import jinja2
import os
import datetime
from models import Business, Coupon, User


__all__ = ['BusinessHandler', 'BusinessIDHandler',
           'BusinessIDAdminHandler', 'BusinessIDUploadHandler']

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    trim_blocks=True)


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

        template = JINJA_ENVIRONMENT.get_template('business_list.html')
        businesses = query.fetch_page(20, projection=[Business.name])[0]
        self.response.status = '200 OK'
        self.response.write(template.render(businesses=businesses,
                                            user=User.query(User.name == 'Dick').get()))


class BusinessIDHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Entity: /business/[id]
    '''
    def get_id(self):
        return int(urllib.unquote(self.request.path.split('/')[2]))

    def get_business(self):
        '''
        Returns business entity, and aborts with code 404 if there's no entity
        '''
        b = Business.get_by_id(self.get_id())
        if b:
            return b
        self.abort(404)

    def get(self):
        '''
        Returns business entity
        '''
        b = self.get_business()
        coupons = Coupon.get_by_business(b.key.id())
        try:
            mark_url = images.get_serving_url(b.mark, size=200)
        except images.BlobKeyRequiredError:
            mark_url = None
        template = JINJA_ENVIRONMENT.get_template('business.html')
        self.response.status = '200 OK'
        self.response.write(template.render(name=b.name,
                                            mark_url=mark_url,
                                            coupons=coupons,
                                            now=datetime.datetime.now(),
                                            user=User.query(User.name == 'Dick').get()))


class BusinessIDAdminHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Entity: /business/[id]/admin
    '''
    def get_id(self):
        return int(urllib.unquote(self.request.path.split('/')[2]))

    def get_business(self):
        '''
        Returns business entity, and aborts with code 404 if there's no entity
        '''
        b = Business.get_by_id(self.get_id())
        if b:
            return b
        self.abort(404)

    def get(self):
        b = self.get_business()
        template = JINJA_ENVIRONMENT.get_template('business_admin.html')
        mark_upload = blobstore.create_upload_url('/business/{}/upload/'
                                                  .format(self.get_id()))
        self.response.status = '200 OK'
        self.response.write(template.render(name=b.name,
                                            mark_upload=mark_upload,
                                            user=User.query(User.name == 'Dick').get()))


class BusinessIDUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    '''
    HTTP Request Handler, Entity: /business/[id]/upload
    '''
    def get_id(self):
        return int(urllib.unquote(self.request.path.split('/')[2]))

    def get_business(self):
        '''
        Returns business entity, and aborts with code 404 if there's no entity
        '''
        b = Business.get_by_id(self.get_id())
        if b:
            return b
        self.abort(404)

    def post(self):
        blob_info = self.get_uploads('mark')[0]
        b = self.get_business()
        b.mark = blob_info.key()
        b.put()
        self.redirect('/business/{}/admin/'.format(self.get_id()))
