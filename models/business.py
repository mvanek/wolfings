from google.appengine.ext import ndb
import json


class Business(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    owners = ndb.StringProperty(repeated=True)

    def to_json(self):
        d = self.to_dict()
        d['location'] = {'lat': d['location'].lat,
                         'lon': d['location'].lon}
        return json.dumps(d)
