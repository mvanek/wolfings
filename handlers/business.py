import webapp2
from google.appengine.api import users
import utils


class BusinessHandler(webapp2.RequestHandler):
    def get(self):
        business_id = utils.path_list(self.request.path)[3]
        print(business_id)

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

    def put(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

    def delete(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
