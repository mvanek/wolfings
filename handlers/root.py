import webapp2
from models import User


class MainHandler(webapp2.RequestHandler):
    def get(self):

        self.response.set_cookie('user_id')

        self.redirect('/coupon/')

    def put(self):
        self.response.write('Hello put!')

    def post(self):
        self.response.write('Hello post!')

    def delete(self):
        self.response.write('Hello delete!')
