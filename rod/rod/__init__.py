import flask
import flask.ext.login
import flask.ext.cors

import rod.extensions
import rod.model

# Models
import rod.model.staff

# Handlers
import rod.handler.auth


def create_app(config):
    app = flask.Flask('Rod')

    # Basic app config
    app.config['SECRET_KEY'] = config['general']['secret_key']

    # Initialize the login extension
    rod.extensions.login_manager.init_app(app)

    # CORSify our Flask using the extension
    flask.ext.cors.CORS(
        app,
        resources='*',
        allow_headers='Content-Type',
        supports_credentials=True
    )

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = config['db']['uri']
    rod.model.db.init_app(app)

    # Register blueprints
    app.register_blueprint(rod.handler.auth.auth)

    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = flask.jsonify(error.to_dict())
        response.status_code = error.status_code

        return response

    return app


class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)

        self.message = message

        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message

        return rv


