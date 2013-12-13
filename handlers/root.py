import webapp2
from RequestHandler import RequestHandler
from google.appengine.api import users


__all__ = ['MainHandler', 'LegalHandler']


class MainHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(MainHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('frontpage.jinja')

    def get(self):
        if users.get_current_user():
            self.redirect('/coupon/')
        self.response.write(self.template.render())


class LegalHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(LegalHandler, self).__init__(*args, **kwargs)
        self.template = self.JINJA_ENVIRONMENT.get_template('legal.jinja')

    def get(self):
        self.response.write(self.template.render())