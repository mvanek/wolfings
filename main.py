import webapp2
from handlers import (MainHandler,
                      AdminHandler,
                      api)
from populate import InitHandler, ReInitHandler


def main():
    return webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/admin', AdminHandler),
        ('/api/user', api.UserHandler),
        ('/api/user/.*', api.UserIDHandler),
        ('/api/coupon', api.CouponHandler),
        ('/api/coupon/.*', api.CouponIDHandler),
        ('/api/business', api.BusinessHandler),
        ('/api/business/.*', api.BusinessIDHandler),
        ('/api/init', InitHandler),
        ('/api/reinit', ReInitHandler)
    ], debug=True)


app = main()
