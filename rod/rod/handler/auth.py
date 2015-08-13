import flask
import flask.ext.login
import flask.ext.bcrypt

import rod
import rod.model.staff


auth = flask.Blueprint('auth', __name__)


@auth.route('/auth', methods=['POST'])
def login():
    staff = rod.model.db.session.query(rod.model.staff.Staff).filter_by(
        email=flask.request.json['email']
    ).first()

    bcrypt = flask.ext.bcrypt.Bcrypt(flask.current_app)

    is_authenticated = bcrypt.check_password_hash(
        staff.password,
        flask.request.json['password']
    )

    if staff and is_authenticated:
        flask.ext.login.login_user(staff)

        staff_schema = rod.model.staff.StaffSchema()

        return flask.jsonify(staff_schema.dump(staff).data)

    raise rod.APIError('Authorization failed', status_code=401)


@auth.route('/auth', methods=['DELETE'])
def logout():
    return flask.request.method


@auth.route('/auth', methods=['GET'])
def verify():
    return flask.request.method
