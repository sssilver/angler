import flask
import os
import yaml
import locale
import logging
import importlib

import rod.request



'''
class Rod(object):

    def __init__(self, config):
        pass  # self.redis = redis.Redis(config['redis_host'], config['redis_port'])

    def dispatch_request(self, request):
        path = [
            node
            for node in request.environ['PATH_INFO'].split('/')[1:]
            if node != ''
        ]

        if len(path) != 2:  # We always expect /module/method
            raise werkzeug.exceptions.BadRequest()

        module = path[0]
        method = path[1]

        try:  # Import the requested module
            module_obj = importlib.import_module('rod.handler.{}'.format(module))
        except ImportError:
            raise werkzeug.exceptions.BadRequest('Module {} not found'.format(module))

        try:  # Load the requested function from the module
            method_obj = getattr(module_obj, method)
        except AttributeError:
            raise werkzeug.exceptions.BadRequest('Method {} not found'.format(method))

        response_body = None
        if request.method != 'OPTIONS':
            response_body = {
                'status': 0,
                'data': method_obj(request, **request.json)
            }

        # Invoke the function with the passed arguments
        try:
            return rod.request.JSONResponse(response_body, {
                'Access-Control-Allow-Origin': request.headers.get('Origin', '*'),
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Headers': ','.join(
                    request.headers.get('Access-Control-Request-Headers', '').split(',') +
                    ['Content-Type']
                )
            })
        except Exception, e:
            raise werkzeug.exceptions.InternalServerError(str(e), str(e))

    def wsgi_app(self, environ, start_response):
        request = rod.request.JSONRequest(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
'''
