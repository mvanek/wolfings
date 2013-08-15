from google.appengine.ext import ndb


class Business(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    owners = ndb.StringProperty(repeated=True)
