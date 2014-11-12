from flask import request, abort, Response
from flask.ext.cors import cross_origin
from flask.ext.login import login_user, logout_user, current_user
from flask.ext.login import LoginManager, login_required
import json
import bcrypt

from rod.db.base import init_db

from rod import app

from rod.model.staff import Staff


@app.route('/init', methods=['GET'])
def init():
    """
    Initialize the database tables
    """

    init_db()
    return 'OK'


@app.route('/api/test', methods=['GET'])
def api_test():
    user = current_user

    print user

    return str(user)


@app.route('/api/login', methods=['POST', 'OPTIONS'])
@cross_origin(headers='Content-Type', send_wildcard=False, supports_credentials=True)
def login():
    credentials = request.get_json()

    print 'logging in %s...' % credentials

    # Authenticate
    if 'email' not in credentials or 'password' not in credentials:
        return unauthorized()

    staff = Staff.query.filter_by(
        email=credentials['email'].lower()
    ).one()

    if not staff:
        return unauthorized()

    print 'User found. Validating password...'

    try:
        hashed_password = bcrypt.hashpw(
            credentials['password'], staff.password
        )

        if hashed_password != staff.password:
            return unauthorized()

        if login_user(staff):
            # TODO: This SA -> dict conversion seems ugly, there must be a better way to do this
            print 'Login successful!'
            staff_dict = staff.__dict__
            del staff_dict['_sa_instance_state']
            del staff_dict['password']

        else:
            print 'Login failure'
            return Response('Login failure', 500)

        return Response(json.dumps(staff_dict), 200)

    except ValueError:
        return Response('', 401)


@app.route('/api/logout', methods=['POST', 'OPTIONS'])
@cross_origin(headers='Content-Type', send_wildcard=False, supports_credentials=True)
@login_required
def logout():
    logout_user()

    return '', 200


@app.route('/api/verify', methods=['GET', 'OPTIONS'])
@cross_origin(headers='Content-Type', send_wildcard=False, supports_credentials=True)
@login_required
def verify():
    # This function is only use to verify that the user is logged in
    return '', 200


@app.route('/api/studentgroup', methods=['POST', 'OPTIONS'])
@cross_origin(headers='Content-Type', send_wildcard=False, supports_credentials=True)
@login_required
def studentgroup_post():
    data = request.get_json()

    print data

    return '', 200


@app.route('/api/studentgroup', methods=['DELETE', 'OPTIONS'])
@cross_origin(headers='Content-Type', send_wildcard=False, supports_credentials=True)
@login_required
def studentgroup_delete():
    data = request.get_json()

    print data

    return '', 200


# Create flask-login's login manager
login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    return Staff.query.get(userid)


@login_manager.unauthorized_handler
def unauthorized():
    return json.dumps({'message': 'Unauthorized, please login'}), 401
