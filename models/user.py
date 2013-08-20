from google.appengine.ext import ndb
import json


class User(ndb.Model):
    name = ndb.StringProperty('n', required=True)
    held_coupons = ndb.KeyProperty('c', kind='Coupon', repeated=True)

    @classmethod
    def list_users(cls, keys_only=False):
        query = cls.query()
        return [user for user in query.iter(keys_only=keys_only)]

    def to_json(self):
        data = self.to_dict()
        data['held_coupons'] = [key.id() for key in data['held_coupons']]
        return json.dumps(data)
