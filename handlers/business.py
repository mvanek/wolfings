import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

import json

import utils
from models import Business, User


class BusinessHandler(webapp2.RequestHandler):
    def get(self):
        business_id = utils.path_list(self.request.path)[3]
        business = ndb.Key("Business", business_id).get()
        if business:
            self.reponse.write(json.dumps(business.to_dict()))
        else:
            self.error(404)
            self.abort()

    def post(self):
        # Authenticate as owner or admin
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            self.abort()

        # Fetch model from datastore
        business_id = utils.path_list(self.request.path)[3]
        business = ndb.Key("Business", business_id).get()
        if user not in business.owners or not user.is_current_user_admin():
            self.error(401)
            self.abort()

        # Verify parameters and change business model
        name = self.request.get('name')
        owners = json.loads(self.request.get('owners'))
        lat = self.request.get('lat')
        lon = self.request.get('lon')
        changed = False
        if name:
            business.name = name
            changed = True
        if owners:
            num_owners = len(owners)
            query = User.query(User.id.IN(owners)).fetch(num_owners)
            if num_owners != len(query):
                self.error(400)
                self.abort()
            business.owners = owners
            changed = True
        if lat and lon:
            if not user.is_current_user_admin():
                self.error(401)
                self.abort()
            if lat > -90 and lat < 90 and lon > -90 and lon < 90:
                business.location = ndb.GeoPt(int(lat), int(lon))
                changed = True

        # Save changes, or throw an error if nothing changed
        if changed:
            business.put()
        else:
            self.error(400)
            self.abort()

    def put(self):
        # Authenticate as admin
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        if not user.is_current_user_admin():
            self.error(401)
            self.abort()

        # Get the parameters
        business_id = utils.path_list(self.request.path)[3]
        name = self.request.get('name')
        owners = json.loads(self.request.get('owners'))
        lat = int(self.request.get('lat'))
        lon = int(self.request.get('lon'))

        # Verify parameters
        if not name or not owners or not lat or not lon:
            self.error(400)
            self.abort()
        if not (lat > -90 and lat < 90 and lon > -90 and lon < 90):
            self.error(400)
            self.abort()
        if owners:
            num_owners = len(owners)
            query = User.query(User.id.IN(owners)).fetch(num_owners)
            if num_owners != len(query):
                self.error(400)
                self.abort()

        # Create new business model and store it.
        business = Business(id=business_id,
                            name=name,
                            location=ndb.GeoPt('{},{}'.format(lat, lon)))
        business.put()

    def delete(self):
        # Authenticate as admin
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        if not user.is_current_user_admin():
            self.error(401)
            return

        # Delete the business model from datastore
        business_id = utils.path_list(self.request.path)[3]
        business = ndb.Key("Business", business_id).get()
        business.delete()
