from google.appengine.ext import ndb
from address import Address
from business import Business
import json


class User(ndb.Model):
    surname       = ndb.StringProperty('s', required=True)
    familiar_name = ndb.StringProperty('f')
    email         = ndb.StringProperty('e', required=True)
    phone         = ndb.IntegerProperty('p')
    address       = ndb.StructuredProperty(Address)
    held_coupons  = ndb.KeyProperty('c', kind='Coupon', repeated=True)
    old_coupons   = ndb.KeyProperty('o', kind='Coupon', repeated=True)

    @property
    def business(self):
        qry = Business.query(Business.admins == self.key)
        return qry.get()

    @classmethod
    def list_users(cls, keys_only=False):
        query = cls.query()
        return [user for user in query.iter(keys_only=keys_only)]

    def dict(self):
        data       = self.to_dict()
        data['id'] = self.key.id()
        try:
            data['held_coupons'] = [key.id() for key in self.held_coupons]
        except ndb.UnprojectedPropertyError:
            pass
        return data

    def json(self):
        return json.dumps(self.dict())
