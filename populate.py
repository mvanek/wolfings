import webapp2
import datetime
from models import Business, Coupon, User


def init(self):
    users = ['Tom', 'Dick', 'Harry']
    coupons = ['Two for one donuts', '50% off coffee', '']
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
        start = datetime.datetime(2013, 1, 1, 0, 0)
        end = datetime.datetime(2013, 2, 1, 0, 0)
        Coupon(name=coupon,
               business=business_key,
               start=start,
               end=end).put()
    self.response.status = '204 No Content'


class InitHandler(webapp2.RequestHandler):
    def get(self):
        init(self)


class ReInitHandler(webapp2.RequestHandler):
    def get(self):
        for b in Business.query().iter():
            b.key.delete()
        for c in Coupon.query().iter():
            c.key.delete()
        for u in User.query().iter():
            u.key.delete()
        init(self)
