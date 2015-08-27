import flask
import flask.ext.login
import flask.ext.bcrypt

import rod
import rod.model.staff


staff = flask.Blueprint('staff', __name__)


@staff.route('/staff', methods=['GET'])
def list_staff():
    all_staff = rod.model.staff.Staff.query.filter_by(is_deleted=False).all()

    return flask.jsonify({
        'items': rod.model.staff.StaffSchema(many=True).dump(all_staff).data,
        'count': len(all_staff)
    })


@staff.route('/staff', methods=['POST'])
def add_staff():
    pass


@staff.route('/staff/<int:staff_id>', methods=['PUT'])
def save_staff(staff_id=None):
    staff_obj = rod.model.staff.StaffSchema().load(flask.request.json).data
    staff_obj.id = staff_id
    rod.model.db.session.merge(staff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.staff.StaffSchema().dump(rod.model.staff.Staff.query.get(staff_id)).data)


@staff.route('/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    staff_obj = rod.model.staff.Staff.query.get(staff_id)

    rod.model.db.session.delete(staff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.staff.StaffSchema().dump(staff_obj).data)
