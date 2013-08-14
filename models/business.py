from google.appengine.ext import ndb


class Business(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPt()
    owners = ndb.UserProperty(repeated=True)
