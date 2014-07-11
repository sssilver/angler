import logging

from flask import Flask, jsonify, request

from flask.ext.restless import APIManager
from db.database import db_session



app = Flask(__name__)
app.config.from_object('config')

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


manager = APIManager(app, session=db_session)


import service.api.models, service.api.calls


blueprints = service.api.models.create_api_blueprints(manager)
for blueprint in blueprints:
    app.register_blueprint(blueprint)
