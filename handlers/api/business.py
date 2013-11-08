import webapp2
from APIHandler import APIHandler
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Business, Coupon


__all__ = ['BusinessHandler', 'BusinessIDHandler']



def authenticate(b=None):
    if users.is_current_user_admin():
        return
    if b and ndb.Key('User', users.get_current_user().user_id()) in b.admins:
        return
    webapp2.abort(401)


class BusinessHandler(APIHandler):
    '''
    HTTP Request Handler, Collection: /api/business
    '''
    def __init__(self, *args, **kwargs):
        super(BusinessHandler, self).__init__(Business, *args, **kwargs)

    def get(self):
        '''
        Returns business URI's, filtered by optional parameters
        Parameters:
            name - Name of the business
            lat,lon - Location of the business
        '''
        params = self.load_http_params({
            'lat': (float, False),
            'lon': (float, False),
            'name': (str, False)
        })

        if 'lat' in params and 'lon' in params:
            query = Business.query_location(
                lat=self.params['lat'],
                lon=self.params['lon']
            )
        else:
            query = Business.query()

        if 'name' in params:
            query = query.filter(Business.name == params['name'])

        self.response.status = '200 OK'
        flag = False
        for key in query.iter(keys_only=True):
            if flag:
                self.response.write('\n')
            else:
                flag = True
            self.response.write(str(key.id()))

    def post(self):
        '''
        Creates a new busines model from posted data
        Returns corresponding URI
        Parameters:
            name - Name of the business
            lat - Lattitude of the business
            lon - Longitude of the business
        '''
        params = self.load_json_params({
            'lat': (float, True),
            'lon': (float, True),
            'name': (str, True),
            'admins': (list, False)
        }, use_default=True)

        authenticate()
        admin_keys = [ndb.Key('User', adm_id) for adm_id in admins]
        if not len(ndb.get_multi(admin_keys)) == len(admin_keys):
            self.abort(400)

        key = Business.new(
            lat=params['lat'],
            lon=params['lon'],
            name=params['name'],
            admins=admin_keys
        ).put()
        uri = '/api/business/{}'.format(key.id())
        self.response.status = '200 OK'
        self.response.write(uri)


class BusinessIDHandler(APIHandler):
    '''
    HTTP Request Handler, Entity: /api/business/[id]
    '''
    def __init__(self, *args, **kwargs):
        super(BusinessIDHandler, self).__init__(Business, *args, **kwargs)

    def get(self):
        '''
        Returns business entity
        '''
        b = self.get_entity()
        self.response.status = '200 OK'
        self.response.content_type = 'application/json'
        self.response.write(b.json())

    def put(self):
        '''
        Modifies business entity at the specified URI from JSON data in
        request body
        '''
        params = self.load_json_params({
            'lat': (float, False),
            'lon': (float, False),
            'name': (str, False),
            'admins': (list, False)
        })

        b = self.get_entity()
        authenticate(b)
        for key, value in params.iteritems():
            if key == 'admins':
                value = [ndb.Key('User', i) for i in value]
            setattr(b, key, value)
        b.gen_geoboxes()
        key = b.put()
        self.response.status = '200 OK'
        self.response.write('/api/business/' + str(key.id()))

    def delete(self):
        '''
        Deletes an existing model
        '''
        b = self.get_entity()
        authenticate(b)
        coupons = Coupon.get_by_business(self.get_id(), keys_only=True)
        if coupons:
            self.response.status = '409 Conflict'
            for c in coupons:
                self.response.write('/api/coupon/{}\n'.format(c.id()))
            return
        b.key.delete()
        self.response.status = '204 No Content'
