import webapp2
from handlers import (SlashHandler,
                      MainHandler,
                      AdminHandler,
                      BusinessHandler,
                      BusinessIDHandler,
                      BusinessIDAdminHandler,
                      api)
from populate import InitHandler, ReInitHandler


def main():
    return webapp2.WSGIApplication([
        ('.*[^/]$', SlashHandler),
        ('/', MainHandler),
        ('/admin/', AdminHandler),
        ('/business/', BusinessHandler),
        ('/business/[0-9]+/', BusinessIDHandler),
        ('/business/[0-9]+/admin/', BusinessIDAdminHandler),
        ('/api/user/', api.UserHandler),
        ('/api/user/.*', api.UserIDHandler),
        ('/api/coupon', api.CouponHandler),
        ('/api/coupon/.*', api.CouponIDHandler),
        ('/api/business/', api.BusinessHandler),
        ('/api/business/.*', api.BusinessIDHandler),
        ('/api/init/', InitHandler),
        ('/api/reinit/', ReInitHandler)
    ], debug=True)


app = main()
