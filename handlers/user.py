import webapp2
from google.appengine.api import users

import json
import urllib

import models


__all__ = ['UserHandler']


def user_exists(user_id):
    query = models.User.get_by_id(user_id)
    return bool(query)


class UserHandler(webapp2.RequestHandler):

    def get_id(self):
        return urllib.unquote(self.request.path.split('/')[3])

    def authenticate(self, user_id=None, admin=False):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            self.abort(401)
        if users.is_current_user_admin():
            return True
        if admin is False and user.user_id() == user_id:
            return True
        self.abort(401)

    def get(self):
        user_id = self.get_id()
        user_model = models.User.get_by_id(user_id)
        try:
            self.response.write(json.dumps(user_model.to_dict()))
        except AttributeError:
            self.abort(404)

    def post(self):
        user_id = self.get_id()
        self.authenticate(user_id)

        name = urllib.unquote(self.request.get('name'))
        if name:
            user_model = models.User.get_by_id(user_id)
            user_model.name = name
            user_model.put()
        else:
            self.abort(400, 'Nothing changed')

    def put(self):
        user_id = self.get_id()
        self.authenticate(admin=True)

        if user_exists(user_id):
            self.abort(400, 'User exists')

        user_model = models.User(id=user_id,
                                 name=urllib.unquote(self.request.get('name')))
        user_model.put()

    def delete(self):
        user_id = self.get_id()
        self.authenticate(admin=True)

        user_model = models.User.get_by_id(user_id)
        if user_model:
            user_model.key.delete()
