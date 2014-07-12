import logging

from flask import Flask, jsonify, request

from flask.ext.restless import APIManager, ProcessingException
from flask.ext.login import current_user, LoginManager

from db.database import db_session



app = Flask(__name__)
app.config.from_object('config')

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Create flask-login's login manager
login_manager = LoginManager()
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
    return Staff.query.get(userid)


def authorize(*args, **kwargs):
    """
        Main Authorization function

        Invoked before every flask-restless request for all HTTP methods

        TODO: implement the difference between 401 and 403
    """

    if not current_user.is_authenticated():
        raise ProcessingException(description='Not Authorized', code=401)


manager = APIManager(
    app,
    session=db_session,
    preprocessors=dict(
        POST=[authorize],
        DELETE=[authorize],
        GET_SINGLE=[authorize],
        GET_MANY=[authorize],
        PATCH_SINGLE=[authorize],
        PATCH_MANY=[authorize]
    )
)


import service.api.models, service.api.calls


blueprints = service.api.models.create_api_blueprints(manager)
for blueprint in blueprints:
    app.register_blueprint(blueprint)