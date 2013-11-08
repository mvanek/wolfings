import logging
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
import json
import urllib
from models import Business, Coupon


__all__ = ['BusinessHandler', 'BusinessIDHandler']


def is_admin(b=None):
    if users.is_current_user_admin():
        return True
    if b:
        logging.info('\nUSER: {}\nADMINS: {}'.format(ndb.Key('User', users.get_current_user().user_id()), b.admins))
        return ndb.Key('User', users.get_current_user().user_id()) in b.admins
    return False


def authenticate(b=None):
    if not is_admin(b):
        webapp2.abort(401)


class BaseBusinessHandler(webapp2.RequestHandler):
    def get_id(self):
        try:
            return self.bid
        except AttributeError:
            self.bid = int(urllib.unquote(self.request.path.split('/')[3]))
        return self.bid

    def get_business(self):
        '''
        Returns business entity, and aborts with code 404 if there's no entity
        '''
        try:
            return self.b
        except AttributeError:
            self.b = Business.get_by_id(self.get_id())
        if not self.b:
            self.b = Business(id=self.get_id())
        return self.b


class BusinessHandler(BaseBusinessHandler):
    '''
    HTTP Request Handler, Collection: /api/business
    '''
    def get(self):
        '''
        Returns business URI's, filtered by optional parameters
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

        self.response.status = '200 OK'
        for key in query.iter(keys_only=True):
            self.response.write(str(key.id()) + '\n')

    def post(self):
        '''
        Creates a new busines model from posted data
        Returns corresponding URI
        Parameters:
            name - Name of the business
            lat - Lattitude of the business
            lon - Longitude of the business
        '''
        authenticate()
        try:
            data = json.loads(self.request.body)
        except ValueError:
            self.abort(400)
        try:
            lat = data['lat']
            lon = data['lon']
            name = data['name']
        except KeyError:
            self.abort(400)
        try:
            lat = float(data.get('lat'))
            lon = float(data.get('lon'))
            name = data.get('lon')
        except ValueError:
            self.abort(400)
        admins = data.get('admins', [])
        admin_keys = [ndb.Key('User', adm_id) for adm_id in admins]
        if not len(ndb.get_multi(admin_keys)) == len(admin_keys):
            self.abort(400)

        b = Business.new(lat=lat, lon=lon, name=name, admins=admin_keys)
        key = b.put()
        uri = '/api/business/{}'.format(key.id())
        self.response.status = '200 OK'
        self.response.write(uri)


class BusinessIDHandler(BaseBusinessHandler):
    '''
    HTTP Request Handler, Entity: /api/business/[id]
    '''
    def get(self):
        '''
        Returns business entity
        '''
        b = self.get_business()
        self.response.status = '200 OK'
        self.response.content_type = 'application/json'
        self.response.write(b.json())

    def put(self):
        '''
        Modifies business entity at the specified URI from JSON data in
        request body
        '''
        b = self.get_business()
        logging.info(b)
        authenticate(b)
        try:
            data = json.loads(self.request.body)
        except ValueError:
            self.abort(400)
        for key, value in data.iteritems():
            if key == 'admins':
                value = [ndb.Key('User', i) for i in value]
            setattr(b, key, value)
        b.gen_geoboxes()
        key = b.put()
        self.response.status = '200 OK'
        self.response.write('/api/business/' + str(key.id()))

    def delete(self):
        '''
        Deletes an existing model
        '''
        b = self.get_business()
        authenticate(b)
        coupons = Coupon.get_by_business(self.get_id(), keys_only=True)
        if coupons:
            self.response.status = '409 Conflict'
            for c in coupons:
                self.response.write('/api/coupon/{}\n'.format(c.id()))
            return
        b.key.delete()
        self.response.status = '204 No Content'
