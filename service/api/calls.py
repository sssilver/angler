from flask import request, abort, jsonify
from flask.ext.cors import cross_origin
from flask.ext.login import login_user, logout_user, current_user
from flask.ext.login import LoginManager, login_required

from db.base import init_db

from service import app

from model.staff import Staff


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

    from model.staff import Staff

    # Authenticate
    staff = Staff.query.filter_by(
        email=credentials['email'].lower(),
        password=credentials['password']
    ).first()

    if staff:
        print 'User found. Logging in...'
        if login_user(staff):
            print 'Login successful!'
            return '', 200
        else:
            print 'Login failure'


    abort(401)


@app.route('/api/logout', methods=['POST', 'OPTIONS'])
@cross_origin(headers='Content-Type', send_wildcard=False, supports_credentials=True)
@login_required
def logout():
    logout_user()

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
    # do stuff
    print 'unauthorized!!!!'
    return '', 401
