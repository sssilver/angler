import flask
import flask.ext.login
import flask.ext.bcrypt

import rod
import rod.model.staff
import rod.model.schemas


staff = flask.Blueprint('staff', __name__)


@staff.route('/staff', methods=['GET'])
def list_staff():
    all_staff = rod.model.staff.Staff.query.filter_by(is_deleted=False).all()

    return flask.jsonify({
        'items': rod.model.schemas.StaffSchema(many=True).dump(all_staff).data,
        'count': len(all_staff)
    })


@staff.route('/staff', methods=['POST'])
def add_staff():
    staff_obj = rod.model.schemas.StaffSchema().load(flask.request.json).data
    rod.model.db.session.add(staff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(staff_obj).data)


@staff.route('/staff/<int:staff_id>', methods=['PUT'])
def save_staff(staff_id=None):
    staff_obj = rod.model.schemas.StaffSchema().load(flask.request.json).data
    staff_obj.id = staff_id

    # Encrypt the password
    password = flask.request.json.get('password')
    if password:
        staff_obj.set_password(password)

    rod.model.db.session.merge(staff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(staff_obj).data)


@staff.route('/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    staff_obj = rod.model.staff.Staff.query.get(staff_id)

    rod.model.db.session.delete(staff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(staff_obj).data)
