import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello get!')
    def put(self):
        self.response.write('Hello put!')
    def post(self):
        self.response.write('Hello post!')
    def delete(self):
        self.response.write('Hello delete!')
