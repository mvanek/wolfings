import webapp2

import json
import urllib

from models import Business


__all__ = ['BusinessHandler', 'BusinessIDHandler']


class BusinessHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler, Collection: /api/business
    '''
    def get(self):
        '''
        Returns business ID's, filtered by optional parameters
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
        self.response.write('[')
        flag = False
        for b in query.iter():
            if flag:
                self.response.write(', ')
            else:
                flag = True
            self.response.write('{{"id":"{}","name":"{}"}}'
                .format(b.key.id(), b.name))
        self.response.write(']')

    def post(self):
        '''
        Creates a new busines model from posted data
        Returns corresponding URI
        Parameters:
            name - Name of the business
            lat - Lattitude of the business
            lon - Longitude of the business
        '''
        try:
            lat = float(urllib.unquote(self.request.get('lat')))
            lon = float(urllib.unquote(self.request.get('lon')))
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
    def get_business_id(self):
        return int(urllib.unquote(self.request.path.split('/')[3]))

    def get_business(self):
        '''
        Returns business entity, and aborts with code 404 if there's no entity
        '''
        id = self.get_business_id()
        b = Business.get_by_id(id)
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

    def put(self):
        '''
        Creates business entity at the specified URI
        The ID must be an integer
        '''
        try:
            data = json.loads(self.request.body)
            b = Business.new(id=self.get_business_id(),
                             name=data['name'],
                             lat=float(data['lat']),
                             lon=float(data['lon']))
        except ValueError:
            self.abort(400)
        self.response.status = '200 OK'
        self.response.write(b.to_json())

    def delete(self):
        '''
        Deletes an existing model
        '''
        b = self.get_business()
        b.key.delete()
        self.response.status = '204 No Content'
