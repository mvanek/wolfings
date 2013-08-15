import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

import json

import utils
from models import Business, User


class BusinessHandler(webapp2.RequestHandler):
    def get(self):
        business_id = utils.path_list(self.request.path)[3]
        business = ndb.Key('Business', business_id).get()
        if business:
            self.reponse.write(json.dumps(business.to_dict()))
        else:
            self.abort(404)

    def post(self):
        # Authenticate as owner or admin
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            self.abort()

        # Fetch model from datastore
        business_id = utils.path_list(self.request.path)[3]
        business = ndb.Key('Business', business_id).get()
        if user not in business.owners or not user.is_current_user_admin():
            self.abort(401)
        changed = False

        # Set business name
        name = self.request.get('name')
        if name:
            business.name = name
            changed = True

        # Set location
        try:
            lat = int(self.request.get('lat'))
            lon = int(self.request.get('lon'))
        except ValueError:
            pass
        else:
            if not user.is_current_user_admin():
                self.abort(401)
            if lat > -90 and lat < 90 and lon > -90 and lon < 90:
                business.location = ndb.GeoPt('{},{}'.format(lat, lon))
                changed = True
            else:
                self.abort(400, 'Invalid lat/lon')

        # Set owners
        try:
            owners = json.loads(self.request.get('owners'))
        except ValueError:
            pass
        else:
            num_owners = len(owners)
            query = User.query(User.id.IN(owners)).fetch(num_owners)
            if num_owners != len(query):
                self.abort(400, 'Invalid owners list')
            business.owners = owners
            changed = True

        # Save changes, or throw an error if nothing changed
        if changed:
            business.put()
        else:
            self.abort(400, 'Nothing changed')

    def put(self):
        # Authenticate as admin
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        if not users.is_current_user_admin():
            self.abort(401)

        # Set ID
        business_id = utils.path_list(self.request.path)[3]

        # Set name
        name = self.request.get('name')
        if not len(name):
            self.abort(400, 'No name given')

        # Set lattitude and longitude
        try:
            lat = int(self.request.get('lat'))
            lon = int(self.request.get('lon'))
        except ValueError:
            self.abort(400, 'Invalid lat/lon: non-integer value')
        if not (lat > -90 and lat < 90 and lon > -90 and lon < 90):
            self.abort(400, 'Invalid lat/lon: bad domain')

        # Set owners
        try:
            owners = json.loads(self.request.get('owners'))
        except ValueError:
            self.abort(400, 'Invalid owner list')
        num_owners = len(owners)
        query = User.query(User.uid.IN(owners)).fetch(num_owners)
        if num_owners != len(query):
            self.abort(400, 'Non-existent users specified')

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
            self.abort(401)
            return

        # Delete the business model from datastore
        business_id = utils.path_list(self.request.path)[3]
        business = ndb.Key("Business", business_id).get()
        business.delete()
