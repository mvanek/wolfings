import webapp2

import json
import urllib

from models import Business, Coupon


__all__ = ['BusinessHandler', 'BusinessIDHandler']


class BusinessHandler(webapp2.RequestHandler):
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
        data = json.loads(self.request.body)
        try:
            lat = float(data['lat'])
            lon = float(data['lon'])
            name = urllib.unquote(self.request.get('name'))
        except ValueError:
            self.abort(500)

        b = Business.new(lat=lat, lon=lon, name=name)
        key = b.put()
        uri = '/api/business/{}'.format(key.id())
        self.response.status = '200 OK'
        self.response.write(uri)


class BusinessIDHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Entity: /api/business/[id]
    '''
    def get_id(self):
        return int(urllib.unquote(self.request.path.split('/')[3]))

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
        self.response.write(b.json())

    def put(self):
        '''
        Modifies business entity at the specified URI from JSON data in
        request body
        '''
        try:
            b = self.get_business()
        except webapp2.HTTPException:
            b = Business(id=self.get_id())
        data = json.loads(self.request.body)
        for key, value in data.iteritems():
            if value:
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
        coupons = Coupon.get_by_business(self.get_id(), keys_only=True)
        if coupons:
            self.response.status = '409 Conflict'
            for c in coupons:
                self.response.write('/api/business/{}\n'.format(c.id()))
            return
        b.key.delete()
        self.response.status = '204 No Content'
