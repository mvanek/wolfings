from google.appengine.ext import ndb
from google.appengine.api import images
from address import Address
import geobox
import json
import logging


class Business(ndb.Model):
    name        = ndb.StringProperty('n', required=True)
    mark        = ndb.BlobKeyProperty('m')
    admins      = ndb.KeyProperty('adm', repeated=True)
    address     = ndb.StructuredProperty(Address, required=True)
    description = ndb.TextProperty('d')
    phone       = ndb.StringProperty('p')
    lat         = ndb.FloatProperty('a', required=True)
    lon         = ndb.FloatProperty('o', required=True)
    geoboxes    = ndb.StringProperty('g', repeated=True)

    @property
    def api_url(self):
        if self.key.id():
            return '/api/business/' + str(self.key.id())
        return None

    @property
    def mark_url(self):
        try:
            return images.get_serving_url(self.mark, size=200)
        except images.BlobKeyRequiredError:
            return None

    @property
    def icon_url(self):
        try:
            return images.get_serving_url(self.mark, size=50)
        except images.BlobKeyRequiredError:
            return None

    def _pre_put_hook(self):
        self.geoboxes = [geobox.compute(self.lat, self.lon, 1, 1)]

    @classmethod
    def query_location(cls, query=None, lat=None, lon=None):
        '''
        Returns a geolocation query that can be further filtered
        '''
        if not query:
            query = Business.query()
        box = geobox.compute(lat, lon, 1, 1)
        query = query.filter(Business.geoboxes == box)
        return query

    def dict(self):
        data = self.to_dict()
        try:
            data['mark'] = images.get_serving_url(self.mark, 200)
        except images.BlobKeyRequiredError:
            data['mark'] = None
        data['id'] = self.key.id()
        del data['geoboxes']
        return data

    def json(self):
        d = self.dict()
        d['admins'] = [user_key.id() for user_key in d['admins']]
        return json.dumps(d)
