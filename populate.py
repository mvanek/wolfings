import webapp2
from models import Business, Coupon, User


class InitHandler(webapp2.RequestHandler):
    def get(self):
        users = ['Tom', 'Dick', 'Harry']
        coupons = ['Free donuts', 'Free coffee', 'Challenge pissing']
        businesses = [('Chipotle', 35.945841, -86.825259),
                      ('Starbucks', 35.960119, -86.802725),
                      ('Dunkin Donuts', 35.959632, -86.801355)]
        for user in users:
            User(name=user).put()
        for business in businesses:
            business_key = Business.new(name=business[0],
                                        lat=business[1],
                                        lon=business[2]).put()
        for coupon in coupons:
            Coupon(name=coupon, business=business_key).put()
        self.response.status = '204 No Content'


class ReInitHandler(webapp2.RequestHandler):
    def get(self):
        query = Business.query()
        for b in query.iter():
            b.gen_geoboxes()
            b.put()
        self.response.status = '204 No Content'
