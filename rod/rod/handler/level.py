import flask

import rod
import rod.model.level
import rod.model.schemas


level_handler = flask.Blueprint('level', __name__)


@level_handler.route('/level', methods=['GET'])
def list_level():
    course_id = flask.request.args.get('course_id')

    query = rod.model.level.Level.query.filter_by(is_deleted=False)

    if course_id:
        levels = query.filter_by(course_id=course_id).all()
    else:
        levels = query.all()

    return flask.jsonify({
        'items': rod.model.schemas.LevelSchema(many=True).dump(levels).data,
        'count': len(levels)
    })


@level_handler.route('/level/<int:level_id>', methods=['GET'])
def get_level(level_id):
    level_obj = rod.model.db.session.query(rod.model.level.Level).get(level_id)

    return flask.jsonify(rod.model.schemas.LevelSchema().dump(level_obj).data)


@level_handler.route('/level/<int:level_id>', methods=['DELETE'])
def delete_level(level_id):
    level_obj = rod.model.level.Level.query.get(level_id)

    rod.model.db.session.delete(level_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(level_obj).data)
