import webapp2
from handlers import (MainHandler,
                      BusinessHandler,
                      BusinessIDHandler,
                      UserHandler)


def main():
    return webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/api/user/.*', UserHandler),
        ('/api/business', BusinessHandler),
        ('/api/business/.*', BusinessIDHandler)
    ], debug=True)


app = main()
