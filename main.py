import webapp2
from handlers import MainHandler, LocationHandler, BusinessHandler, UserHandler


def main():
    return webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/api/location', LocationHandler),
        ('/api/user/.*', UserHandler),
        ('/api/business/.*', BusinessHandler)
    ], debug=True)


app = main()
