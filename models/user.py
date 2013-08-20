from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty('n', required=True)
    held_coupons = ndb.KeyProperty('c', kind='Coupon', repeated=True)

    def list_users(cls, keys_only=False):
        query = cls.query(keys_only=keys_only)
        return [user for user in query.iter()]
