import flask
import flask.ext.login
import flask.ext.bcrypt

import rod
import rod.model.staff


auth = flask.Blueprint('auth', __name__)


@auth.route('/auth', methods=['GET'])
def verify():
    staff = flask.ext.login.current_user

    if staff.is_authenticated():
        return flask.jsonify(rod.model.staff.StaffSchema().dump(staff).data)


@auth.route('/auth', methods=['POST'])
def login():
    staff = rod.model.db.session.query(rod.model.staff.Staff).filter_by(
        email=flask.request.json['email']
    ).first()

    if staff is None:
        # User doesn't exist
        # Instantiate a fake user to cycle through the whole authentication process
        staff = rod.model.staff.Staff()
        staff.password = flask.ext.bcrypt.generate_password_hash('any pass')  # Whatever
        # Authentication will fail even if the typed password matches the one above,
        # due to staff check

    bcrypt = flask.ext.bcrypt.Bcrypt(flask.current_app)

    is_password_correct = bcrypt.check_password_hash(
        staff.password,
        flask.request.json['password']
    )

    if staff and is_password_correct:
        flask.ext.login.login_user(staff)

        staff_schema = rod.model.staff.StaffSchema()

        return flask.jsonify(staff_schema.dump(staff).data)

    raise rod.APIError('Authorization failed', status_code=401)


@auth.route('/auth', methods=['DELETE'])
def logout():
    flask.ext.login.logout_user()

    return ''
