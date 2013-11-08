import webapp2
import json
import urllib


__all__ = ['APIHandler']


class APIHandler(webapp2.RequestHandler):
    def __init__(self, entity, *args, **kwargs):
        super(APIHandler, self).__init__(*args, **kwargs)
        self.entity = entity

    def _load_params(self, data, param_info, use_default):
        params = {}
        for k,(dtype,required) in param_info.iteritems():
            try:
                params[k] = dtype(data[k])
            except ValueError:
                self.abort(400)
            except KeyError:
                if required:
                    self.abort(400)
                if use_default:
                    params[k] = dtype()
        self.params = params
        return self.params

    def load_json_params(self, param_info, use_default=False):
        try:
            data = json.loads(self.request.body)
        except ValueError:
            self.abort(400)
        return self._load_params(data, param_info, use_default)

    def load_http_params(self, param_info, use_default=False):
        return self._load_params(self.request.params, param_info, use_default)

    def get_id(self):
        try:
            return self.eid
        except AttributeError:
            self.eid = int(urllib.unquote(self.request.path.split('/')[3]))
        return self.eid

    def get_entity(self):
        '''
        Returns business entity, and aborts with code 404 if there's no entity
        '''
        try:
            return self.b
        except AttributeError:
            self.b = self.entity.get_by_id(self.get_id())
        if not self.b:
            self.b = self.entity(id=self.get_id())
        return self.b
