import webapp2


__all__ = ['SlashHandler']


class SlashHandler(webapp2.RequestHandler):
    '''
    Forces all URLs to end with a slash
    '''
    def get(self):
        '''
        HTTP GET Method Handler
        Parameters: None
        '''
        self.redirect(self.request.path + '/', permanent=True)
