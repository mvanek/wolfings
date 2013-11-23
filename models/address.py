from google.appengine.ext import ndb


class Address(ndb.Model):
    number = ndb.IntegerProperty()
    street = ndb.StringProperty()
    city = ndb.StringProperty()
    state = ndb.StringProperty()
    zip = ndb.StringProperty()
    country = ndb.StringProperty()