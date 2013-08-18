from google.appengine.ext import ndb
from business import Business


class Coupon(ndb.Model):
    business = ndb.KeyProperty('b', required=True, kind=Business)
    name = ndb.StringProperty('n', required=True)
    description = ndb.TextProperty('d', required=True)
