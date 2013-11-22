import webapp2
from RequestHandler import RequestHandler
from models import User
from google.appengine.api import users
import logging

__all__ = ['LoginHandler',
           'LogoutHandler',
           'RegisterHandler']


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            user_model = User.get_by_id(user.user_id())
            if user_model is None:
                logging.info('User model is None')
                self.redirect('/register/')
                return
            logging.info('User model is NOT None')
            self.redirect('/')
            return
        self.redirect(users.create_login_url(dest_url='/login/'))


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
        self.redirect(users.create_logout_url('/'))


class RegisterHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(RegisterHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('register.jinja')

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/login/')
        self.status = '200 OK'
        self.response.write(self.template.render())

    def post(self):
        self.load_http_params({
            'name': (str, True),
            'phone': (int, False)
        }, use_default=True)
        user = users.get_current_user()
        user_model = User(
            id=user.user_id(),
            name=self.params['name'],
            phone=self.params['phone'],
            email=user.email()
        )
        user_model.put()
        self.redirect('/')
