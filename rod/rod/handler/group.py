import flask

import rod
import rod.model.group
import rod.model.schemas


group = flask.Blueprint('group', __name__)


@group.route('/group', methods=['GET'])
def list_group():
    teacher_id = flask.request.args.get('teacher_id')

    query = rod.model.group.Group.query.filter_by(is_deleted=False)

    if teacher_id:
        groups = query.filter_by(teacher_id=teacher_id).all()
    else:
        groups = query.all()

    return flask.jsonify({
        'items': rod.model.schemas.GroupSchema(many=True).dump(groups).data,
        'count': len(groups)
    })


@group.route('/group/<int:group_id>', methods=['GET'])
def get_group(group_id):
    group_obj = rod.model.db.session.query(rod.model.group.Group).get(group_id)

    return flask.jsonify(rod.model.schemas.GroupSchema().dump(group_obj).data)


@group.route('/group', methods=['POST'])
def add_group():
    group_obj = rod.model.schemas.GroupSchema().load(flask.request.json).data

    rod.model.db.session.add(group_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.GroupSchema().dump(group_obj).data)


@group.route('/group/<int:group_id>', methods=['PUT'])
def save_group(group_id):
    group_obj = rod.model.schemas.GroupSchema().load(flask.request.json).data
    group_obj.id = group_id

    rod.model.db.session.merge(group_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.GroupSchema().dump(group_obj).data)


@group.route('/group/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    group_obj = rod.model.group.Group.query.get(group_id)

    rod.model.db.session.delete(group_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(group_obj).data)
