import webapp2
from handlers import MainHandler, LocationHandler, BusinessHandler


def main():
    return webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/api/location', LocationHandler),
        ('/api/business/.*', BusinessHandler)
    ], debug=True)


app = main()
