import logging
import webapp2
import urllib
import jinja2
import os
from models import Business


__all__ = ['BusinessHandler', 'BusinessIDHandler']

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'])


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
        self.response.write(template.render(businesses=businesses))


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
        template = JINJA_ENVIRONMENT.get_template('business.html')
        self.response.status = '200 OK'
        self.response.write(template.render(name=b.name))


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
        '''
        Returns business entity
        '''
        b = self.get_business()
        self.response.status = '200 OK'
        self.response.write(b.to_json())
