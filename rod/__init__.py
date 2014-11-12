import logging

from flask import Flask, jsonify, request

from flask.ext.restless import APIManager, ProcessingException
from flask.ext.login import current_user

from db.database import Database


app = Flask(__name__)
app.config.from_object('rod.config')
app.db = Database(app.config['SQLALCHEMY_DATABASE_URI'])

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


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
    session=app.db.session,
    preprocessors=dict(
        POST=[authorize],
        DELETE=[authorize],
        GET_SINGLE=[authorize],
        GET_MANY=[authorize],
        PATCH_SINGLE=[authorize],
        PATCH_MANY=[authorize]
    )
)

import api.models
import api.calls


blueprints = api.models.create_api_blueprints(manager)
for blueprint in blueprints:
    app.register_blueprint(blueprint)
