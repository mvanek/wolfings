from google.appengine.ext import ndb
from coupon import Coupon


class User(ndb.Model):
    name = ndb.StringProperty('n', required=True)
    held_coupons = ndb.KeyProperty('c',
                                   kind=Coupon,
                                   repeated=True)
