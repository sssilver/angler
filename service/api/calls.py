from flask import request, abort, jsonify
from flask.ext.cors import cross_origin
from flask.ext.login import login_user

from db.base import init_db

from model.staff import Staff

from service import app


@app.route('/init', methods=['GET'])
def init():
    """
    Initialize the database tables
    """

    init_db()
    return 'OK'


@app.route('/api/login', methods=['POST', 'OPTIONS'])
@cross_origin(headers='Content-Type')
def login():
    credentials = request.get_json()

    # Authenticate
    staff = Staff.query.filter_by(
        email=credentials['email'].lower(),
        password=credentials['password']
    ).first()

    if staff:
        login_user(staff)

        return '', 200


    abort(401)

