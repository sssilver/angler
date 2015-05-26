import tornado.web
import functools
import simplejson

import rod.serialize


class CorsHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Headers', ','.join(
            self.request.headers.get('Access-Control-Request-Headers', '').split(',') +
            ['Content-Type']
        ))

        super(CorsHandler, self).set_default_headers()

    def options(self, *args, **kwargs):
        pass


class BaseHandler(CorsHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def config(self):
        return self.application.config

    def get_current_user(self):
        # Returns the currently authenticated user based on the cookie
        return self.get_secure_cookie('user')

    def get_login_url(self):
        return ''

    def write(self, chunk):
        super(BaseHandler, self).write(simplejson.dumps(chunk, cls=rod.serialize.JSONEncoder))


def auth(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper
