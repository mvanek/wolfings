import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

import json
import urllib

import models


def users_exist(user_ids):
    ret = True
    keys = [ndb.Key('User', uid) for uid in user_ids]
    for user in ndb.get_multi(keys):
        ret = ret and bool(user)
    return ret


class BusinessHandler(webapp2.RequestHandler):

    def get_id(self):
        return urllib.unquote(self.request.path.split('/')[3])

    def authenticate(self, user_ids=[], admin=False):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            self.abort()
        if users.is_current_user_admin():
            return True
        if admin is False and user.user_id() in user_ids:
            return True
        self.abort(401)

    def get_location(self):
        try:
            lat = int(urllib.unquote(self.request.get('lat')))
            lon = int(urllib.unquote(self.request.get('lon')))
        except ValueError:
            return None
        if lat < -90 or lat > 90 or lon < -90 or lon > 90:
            return None
        return ndb.GeoPt('{},{}'.format(lat, lon))

    def get_name(self):
        return urllib.unquote(self.request.get('name'))

    def get_owners(self):
        try:
            owners = json.loads(urllib.unquote(self.request.get('owners')))
        except ValueError:
            return []
        else:
            if not users_exist(owners):
                self.abort(400, 'Nonexistent owners')
        return owners

    def get(self):
        business_id = self.get_id()
        business = models.Business.get_by_id(business_id)
        try:
            self.response.write(business.to_json())
        except AttributeError:
            self.abort(404)

    def post(self):
        business_id = self.get_id()
        business = models.Business.get_by_id(business_id)
        if not business:
            self.abort(404)
        self.authenticate(business.owners)

        name = self.get_name()
        if name:
            business.name = name

        location = self.get_location()
        if location:
            self.authenticate(admin=True)
            business.location = location

        owners = self.get_owners()
        if owners:
            business.owners = owners

        if not (name or location or owners):
            self.abort(
                400,
                'Incomplete request:\n'
                'name: {}\n'
                'location: {}\n'
                'owners: {}'.format(name, location, owners))
        business.put()

    def put(self):
        self.authenticate(admin=True)

        business_id = self.get_id()
        name = self.get_name()
        location = self.get_location()
        owners = self.get_owners()
        if not (name and location and owners):
            self.abort(
                400,
                'Incomplete request:\n'
                'name: {}\n'
                'location: {}\n'
                'owners: {}'.format(name, location, owners))

        business = models.Business(id=business_id,
                                   name=name,
                                   location=location,
                                   owners=owners)
        business.put()

    def delete(self):
        self.authenticate(admin=True)
        ndb.Key('Business', self.get_id()).delete()
