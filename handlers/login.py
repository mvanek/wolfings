import webapp2
from models import User
from google.appengine.api import users


__all__ = ['LoginHandler',
           'LogoutHandler']


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            user_model = User.get_by_id(user.user_id())
            if not user_model:
                user_model = User(id=user.user_id(),
                                  name=user.nickname(),
                                  email=user.email())
                user_model.put()
            self.redirect('/')
            return
        self.redirect(users.create_login_url(dest_url='/login/'))

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
        self.redirect(users.create_logout_url('/'))
