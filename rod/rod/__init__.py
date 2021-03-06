import flask
import flask.ext.login
import flask.ext.cors

# Models
import rod.model.company
import rod.model.course
import rod.model.group
import rod.model.lesson
import rod.model.level
import rod.model.staff
import rod.model.student
import rod.model.comment
import rod.model.tariff
import rod.model.transaction

import rod.model.schemas

import rod.extensions
import rod.model

# Handlers
import rod.handler.auth
import rod.handler.staff
import rod.handler.course
import rod.handler.tariff
import rod.handler.level
import rod.handler.student
import rod.handler.company
import rod.handler.group
import rod.handler.credit
import rod.handler.lesson


def create_app(config):
    app = flask.Flask('Rod')

    # Basic app config
    app.config['SECRET_KEY'] = config['general']['secret_key']
    app.config['DEBUG'] = config['general']['debug']

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
    blueprints = {
        rod.handler.auth.auth_handler,
        rod.handler.staff.staff_handler,
        rod.handler.course.course_handler,
        rod.handler.tariff.tariff_handler,
        rod.handler.level.level_handler,
        rod.handler.student.student_handler,
        rod.handler.company.company_handler,
        rod.handler.group.group_handler,
        rod.handler.credit.credit_handler,
        rod.handler.lesson.lesson_handler
    }

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

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


