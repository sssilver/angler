from flask import request, abort, jsonify
from flask.ext.cors import cross_origin

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


@app.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(headers='Content-Type')
def login():
    credentials = request.get_json()

    # Authenticate
    staff = Staff.query.filter_by(email=credentials['email'].lower()).first()

    if staff and staff.authenticate(credentials['password']):
        return jsonify(staff)

    abort(401)

