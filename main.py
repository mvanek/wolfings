import webapp2
from handlers import MainHandler, LocationHandler, BusinessHandler


def main():
    webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/api/location', LocationHandler)
        ('/api/business/.*', BusinessHandler)
    ], debug=True)


if __name__ == '__main__':
    main()
