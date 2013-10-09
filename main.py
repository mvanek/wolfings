import webapp2
from handlers import (SlashHandler,
                      MainHandler,
                      AdminHandler,
                      CouponHandler,
                      CouponIDHandler,
                      BusinessHandler,
                      BusinessIDHandler,
                      BusinessIDAdminHandler,
                      BusinessIDAdminCouponHandler,
                      BusinessIDUploadHandler,
                      UserHandler,
                      UserIDHandler,
                      UserIDAdminHandler,
                      api)
from populate import InitHandler, ReInitHandler


def main():
    return webapp2.WSGIApplication([
        ('/api/user/',                      api.UserHandler),
        ('/api/user/[0-9]+',                api.UserIDHandler),
        ('/api/user/[0-9]+/coupons/',       api.UserIDCouponHandler),
        ('/api/user/[0-9]+/coupons/[0-9]+', api.UserIDCouponIDHandler),
        ('/api/coupon/',                    api.CouponHandler),
        ('/api/coupon/[0-9]+',              api.CouponIDHandler),
        ('/api/business/',                  api.BusinessHandler),
        ('/api/business/[0-9]+',            api.BusinessIDHandler),
        ('/api/init/',                      InitHandler),
        ('/api/reinit/',                    ReInitHandler),

        ('.*[^/]$', SlashHandler),
        ('/',       MainHandler),
        ('/admin/', AdminHandler),

        ('/coupon/',                        CouponHandler),
        ('/coupon/[0-9]+/',                 CouponIDHandler),
        ('/business/',                      BusinessHandler),
        ('/business/[0-9]+/',               BusinessIDHandler),
        ('/business/[0-9]+/admin/',         BusinessIDAdminHandler),
        ('/business/[0-9]+/admin/coupons/', BusinessIDAdminCouponHandler),
        ('/business/[0-9]+/upload/',        BusinessIDUploadHandler),
        ('/user/',                          UserHandler),
        ('/user/[0-9]+/',                   UserIDHandler),
        ('/user/[0-9]+/admin/',             UserIDAdminHandler)
    ], debug=True)


app = main()
