import jinja2
import os
import webapp2


__all__ = ['AdminHandler']

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'])


class AdminHandler(webapp2.RequestHandler):
    '''
    HTTP Request Handler: /api/coupon
    '''
    def get(self):
        '''
        HTTP GET Method Handler
        Parameters: None
        '''
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.status = '200 OK'
        self.response.write(template.render())
