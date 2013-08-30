import webapp2
from handlers import (MainHandler,
                      BusinessHandler,
                      BusinessIDHandler,
                      CouponHandler,
                      CouponIDHandler,
                      UserHandler,
                      UserIDHandler)
from populate import InitHandler, ReInitHandler


def main():
    return webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/api/user', UserHandler),
        ('/api/user/.*', UserIDHandler),
        ('/api/coupon', CouponHandler),
        ('/api/coupon/.*', CouponIDHandler),
        ('/api/business', BusinessHandler),
        ('/api/business/.*', BusinessIDHandler),
        ('/api/init', InitHandler),
        ('/api/reinit', ReInitHandler)
    ], debug=True)


app = main()
