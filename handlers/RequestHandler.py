import logging
import webapp2
import urllib
import jinja2
import os
import datetime
from models import User
from google.appengine.ext import ndb
from google.appengine.api import users


__all__ = ['RequestHandler',
           'get_cur_user']

TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'jinja2'
)


def get_cur_user():
    user = users.get_current_user()
    if user:
        return User.get_by_id(user.user_id())
    return None

@jinja2.environmentfunction
def is_admin(env, b=None):
    if users.is_current_user_admin():
        return True
    if b and env.globals['user']:
        return env.globals['user'].key in b.admins
    return False

def timedelta(t):
    hours = t.seconds//3600
    minutes = (t.seconds - 3600*hours)//60
    seconds = t.seconds - 60*minutes - 3600*hours
    return '{}:{:02}:{:02}'.format(t.days*24+hours, minutes, seconds)

def stringify_unit(v,u):
    return '{} {}{}'.format(v, u, 's' if v!=1 else '')

def timedelta_verbose(t):
    hours   = t.seconds//3600
    minutes = (t.seconds - 3600*hours)//60
    seconds = t.seconds - 60*minutes - 3600*hours
    stringlist = []
    if t.days:
        stringlist.append(stringify_unit(t.days, 'day'))
    if hours:
        stringlist.append(stringify_unit(hours, 'hour'))
    if minutes:
        stringlist.append(stringify_unit(minutes, 'minute'))
    if seconds:
        stringlist.append(stringify_unit(seconds, 'second'))
    llen = len(stringlist)
    if llen > 1:
        return '{} and {}'.format(', '.join(stringlist[0:llen-1]), stringlist[llen-1])
    return stringlist[0]

def dt(v):
    return v.strftime('%c') + ' GMT'


class RequestHandler(webapp2.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(RequestHandler, self).__init__(*args, **kwargs)
        self.JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
            extensions=['jinja2.ext.autoescape'],
            trim_blocks=True
        )
        cur_user = get_cur_user()
        self.JINJA_ENVIRONMENT.globals['users']             = users
        self.JINJA_ENVIRONMENT.globals['user']              = cur_user
        self.JINJA_ENVIRONMENT.globals['now']               = datetime.datetime.now()
        self.JINJA_ENVIRONMENT.globals['is_admin']          = is_admin
        self.JINJA_ENVIRONMENT.filters['timedelta']         = timedelta
        self.JINJA_ENVIRONMENT.filters['timedelta_verbose'] = timedelta_verbose
        self.JINJA_ENVIRONMENT.filters['datetime']          = dt

    def _load_params(self, data, param_info, use_default):
        params = {}
        for k,(dtype,required) in param_info.iteritems():
            logging.info('Unpacking '+k)
            try:
                params[k] = dtype(data[k])
            except (ValueError, TypeError):
                if required or data[k]:
                    logging.info('Exception occured when converting '+data[k])
                    self.abort(400)
                if use_default:
                    params[k] = dtype()
            except KeyError:
                if required:
                    self.abort(400)
                if use_default:
                    params[k] = dtype()
        self.params = params

    def load_json_params(self, param_info, use_default=False):
        try:
            data = json.loads(self.request.body)
        except ValueError:
            self.abort(400)
        return self._load_params(data, param_info, use_default)

    def load_http_params(self, param_info, use_default=False):
        return self._load_params(self.request.params, param_info, use_default)

    def get_page_id(self):
        pathparts = urllib.unquote(self.request.path).split('/')
        return pathparts[2]

    def get_page_key(self):
        pathparts = urllib.unquote(self.request.path).split('/')
        path_len = len(pathparts)
        page_id = pathparts[2]
        page_modelname = pathparts[1].capitalize()
        key = ndb.Key(page_modelname, self.idtype(page_id))
        return key

    def get_page_entity(self):
        key = self.get_page_key()
        entity = key.get()
        if not entity:
            self.abort(404)
        return entity

    def render(self, *args, **kwargs):
        self.response.write(self.template.render(*args, **kwargs))
