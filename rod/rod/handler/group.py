import flask

import rod
import rod.model.group
import rod.model.student
import rod.model.schemas


group_handler = flask.Blueprint('group', __name__)


@group_handler.route('/group', methods=['GET'])
def list_group():
    teacher_id = flask.request.args.get('teacher_id')
    level_id = flask.request.args.get('level_id')

    query = rod.model.group.Group.query.filter_by(is_deleted=False)

    if teacher_id:
        query = query.filter_by(teacher_id=teacher_id)

    if level_id:
        query = query.filter_by(level_id=level_id)

    groups = query.all()

    return flask.jsonify({
        'items': rod.model.schemas.GroupSchema(many=True).dump(groups).data,
        'count': len(groups)
    })


@group_handler.route('/group/<int:group_id>', methods=['GET'])
def get_group(group_id):
    group = rod.model.db.session.query(rod.model.group.Group).get(group_id)

    return flask.jsonify(rod.model.schemas.GroupSchema().dump(group).data)


@group_handler.route('/group', methods=['POST'])
def add_group():
    group = rod.model.schemas.GroupSchema().load(flask.request.json).data

    rod.model.db.session.add(group)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.GroupSchema().dump(group).data)


@group_handler.route('/group/<int:group_id>/students', methods=['POST'])
def add_students_to_group(group_id):
    # Add each student to the group with their respective tariff
    for member in flask.request.json:
        membership = rod.model.student.Membership()
        membership.student_id = member['student_id']
        membership.tariff_id = member['tariff_id']
        membership.group_id = group_id

        rod.model.db.session.add(membership)

    rod.model.db.session.commit()  # Execute all together

    group = rod.model.db.session.query(rod.model.group.Group).get(group_id)

    return flask.jsonify(rod.model.schemas.GroupSchema().dump(group).data)


@group_handler.route('/group/<int:group_id>', methods=['PUT'])
def save_group(group_id):
    group = rod.model.schemas.GroupSchema().load(flask.request.json).data
    group.id = group_id

    rod.model.db.session.merge(group)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.GroupSchema().dump(group).data)


@group_handler.route('/group/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    group = rod.model.group.Group.query.get(group_id)

    rod.model.db.session.delete(group)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(group).data)
