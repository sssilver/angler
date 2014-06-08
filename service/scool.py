import logging

from flask import Flask, jsonify, request
from api import create_api_blueprints

from db.database import db_session
from db.base import init_db
from flask.ext.cors import cross_origin
from flask.ext.restless import APIManager

from model.student import Student
from model.level import Level

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_object('config')

manager = APIManager(app, session=db_session)

blueprints = create_api_blueprints(manager)
for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.route('/init', methods=['GET'])
def init():
    """
    Initialize the database tables
    """

    init_db()
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
