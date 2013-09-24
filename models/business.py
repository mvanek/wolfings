from google.appengine.ext import ndb
import geobox
import json


class Business(ndb.Model):
    name = ndb.StringProperty('n', required=True)
    lat = ndb.FloatProperty('a', required=True)
    lon = ndb.FloatProperty('o', required=True)
    geoboxes = ndb.StringProperty('g', repeated=True)

    @classmethod
    def new(cls, **kwargs):
        b = Business(**kwargs)
        b.gen_geoboxes()
        return b

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

    def gen_geoboxes(self):
        self.geoboxes = [geobox.compute(self.lat, self.lon, 1, 1)]

    def to_json(self):
        data = self.to_dict()
        data['id'] = self.key.id()
        #del data['geoboxes']
        return json.dumps(data)
