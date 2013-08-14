import webapp2


class LocationHandler(webapp2.RequestHandler):
    def get(self):
        pass

    def post(self):
        self.error(405)

    def put(self):
        self.error(405)

    def delete(self):
        self.error(405)
