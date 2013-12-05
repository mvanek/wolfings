import webapp2
from RequestHandler import RequestHandler, get_cur_user
from models import User, ProtoBusiness
from google.appengine.api import users
import logging

__all__ = ['LoginHandler',
           'LogoutHandler',
           'RegisterHandler',
           'LegalHandler',
           'PartnerHandler']


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
            'surname': (str, True),
            'firstName': (str, False),
            'phone': (int, False)
        }, use_default=True)
        user = users.get_current_user()
        user_model = User(
            id=user.user_id(),
            surname=self.params['surname'],
            familiar_name=self.params['firstName'],
            phone=self.params['phone'],
            email=user.email()
        )
        user_model.put()
        self.redirect('/')


class LegalHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(LegalHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('legal.jinja')

    def get(self):
        self.response.write(self.template.render())


class PartnerHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(PartnerHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('partner.jinja')

    def get(self):
        user = get_cur_user()
        if not user:
            self.redirect('/login/')
        self.response.write(self.template.render())

    def post(self):
        user = get_cur_user()
        if not user:
            self.redirect('/login/')
        self.load_http_params({
            'address': (str, False),
            'city': (str, False),
            'zip': (str, False),
            'name': (str, False),
            'phone': (str, False),
            'cname': (str, False),
            'cemail': (str, False),
            'cphone': (str, False)
        }, use_default=True)
        b = ProtoBusiness(
            initiator=user.key,
            name=self.params['name'],
            address='{} {} {}'.format(
                self.params['address'],
                self.params['city'],
                self.params['zip']
            ),
            cname=self.params['cname'],
            cemail=self.params['cemail'],
            cphone=self.params['cphone']
        )
        b.put()
        self.response.write(self.template.render(post=True))