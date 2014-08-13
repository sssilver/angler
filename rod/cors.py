from flask import request


allowed_origins = [
    'http://localhost',
    'http://scool.org',
    'http://www.scool.org'
]

def add_cors_headers(response):
    # Only allow CORS requests from our trusted origins specified above
    try:
        origin = request.headers['Origin']

        if origin not in allowed_origins:
            raise KeyError

    except KeyError:
        return response

    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'HEAD, GET, POST, PATCH, PUT, OPTIONS, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response