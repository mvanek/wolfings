from google.appengine.ext import ndb
import json
from business import Business
from user import User


class Coupon(ndb.Model):
    name = ndb.StringProperty('n', required=True)
    business = ndb.KeyProperty('b', required=True, kind='Business')
    start = ndb.DateTimeProperty('s', required=True)
    end = ndb.DateTimeProperty('e', required=True)

    @classmethod
    def get_all(cls, time=None, keys_only=False):
        '''
        Returns a list of all coupons
        '''
        query = Coupon.query()
        if time:
            query = query.filter(cls.end > time)
        return [c for c in query.iter(keys_only=keys_only)]

    @classmethod
    def get_by_business(cls, business_id, time=None, keys_only=False):
        '''
        Returns a list of all coupons
        '''
        query = Coupon.query(cls.business == ndb.Key(Business, business_id))
        if time:
            query = query.filter(cls.end > time)
        return [c for c in query.iter(keys_only=keys_only)]

    @classmethod
    def get_by_user(cls, user_id, keys_only=False):
        '''
        Returns a list of all coupons
        '''
        user = User.get_by_id(user_id)
        coupon_keys = user.held_coupons
        if keys_only:
            return coupon_keys
        else:
            return ndb.get_multi(coupon_keys)

    @classmethod
    def get_by_user_and_business(cls, user_id, business_id, time=None,
                                 keys_only=False):
        '''
        Returns a list of all coupons
        '''
        user_coupons = set(cls.get_by_user(user_id, keys_only=keys_only))
        business_coupons = set(cls.get_by_business(business_id,
                                                   time=time,
                                                   keys_only=keys_only))
        return user_coupons & business_coupons

    @classmethod
    def list_coupons(cls, user_id=None, business_id=None, time=None,
                     keys_only=False):
        '''
        Filters by provided parameters
        '''
        if user_id and business_id:
            return cls.get_by_user_and_busines(user_id=user_id,
                                               business_id=business_id,
                                               time=time,
                                               keys_only=keys_only)
        if user_id:
            return cls.get_by_user(user_id=user_id,
                                   keys_only=keys_only)
        if business_id:
            return cls.get_by_business(business_id=business_id,
                                       time=time,
                                       keys_only=keys_only)
        return cls.get_all(time=time, keys_only=keys_only)

    def dict(self):
        data = self.to_dict()
        data['id'] = self.key.id()
        data['business'] = data['business'].id()
        return data

    def json(self):
        data = self.dict()
        data['start'] = data['start'].strftime('%Y-%m-%dT%H:%M:%S.000Z')
        data['end'] = data['end'].strftime('%Y-%m-%dT%H:%M:%S.000Z')
        return json.dumps(data)

    def delete(self):
        users = User.query(User.held_coupons == self.key)
        users.held_coupons.remove(self.key)
        users.put()
        self.key.delete()
