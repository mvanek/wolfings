from google.appengine.ext import ndb
import geobox
import json
import logging


class Business(ndb.Model):
    name = ndb.StringProperty('n', required=True)
    lat = ndb.FloatProperty('a', required=True)
    lon = ndb.FloatProperty('o', required=True)
    geoboxes = ndb.StringProperty('g', repeated=True)

    @classmethod
    def new(self, **kwargs):
        b = Business(**kwargs)
        b.gen_geoboxes()
        return b

    @classmethod
    def query_location(self, lat, lon):
        '''
        Returns a geolocation query that can be further filtered
        '''
        box = geobox.compute(lat, lon, 8, 25)
        query = Business.query(Business.geoboxes == box)
        logging.error('Box: {}'.format(box))
        return query

    def gen_geoboxes(self):
        self.geoboxes = [geobox.compute(self.lat, self.lon, 8, 25)]

    def to_json(self):
        data = self.to_dict()
        #del data['geoboxes']
        return json.dumps(data)
