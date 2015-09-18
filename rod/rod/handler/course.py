import flask

import rod
import rod.model.course
import rod.model.level
import rod.model.schemas


course_handler = flask.Blueprint('course', __name__)


@course_handler.route('/course', methods=['GET'])
def list_course():
    all_courses = rod.model.course.Course.query.filter_by(is_deleted=False).all()

    return flask.jsonify({
        'items': rod.model.schemas.CourseSchema(many=True).dump(all_courses).data,
        'meta': {'count': len(all_courses)}
    })


@course_handler.route('/course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course_obj = rod.model.db.session.query(rod.model.course.Course).get(course_id)

    return flask.jsonify(rod.model.schemas.CourseSchema().dump(course_obj).data)


@course_handler.route('/course', methods=['POST'])
def add_course():
    course = rod.model.schemas.CourseSchema().load(flask.request.json).data
    rod.model.db.session.add(course)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.CourseSchema().dump(course).data)


@course_handler.route('/course/<int:course_id>', methods=['PUT'])
def save_course(course_id):
    course = rod.model.schemas.CourseSchema().load(flask.request.json).data
    course.id = course_id

    rod.model.db.session.merge(course)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.CourseSchema().dump(course).data)


@course_handler.route('/course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = rod.model.course.Course.query.get(course_id)

    rod.model.db.session.delete(course)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(course).data)


@course_handler.route('/course/<int:course_id>/level', methods=['POST'])
def add_level(course_id):
    level = rod.model.schemas.LevelSchema().load(flask.request.json).data
    level.course_id = course_id

    rod.model.db.session.add(level)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.LevelSchema().dump(level).data)


@course_handler.route('/course/<int:course_id>/level', methods=['GET'])
def list_level(course_id):
    query = rod.model.level.Level.query.filter_by(is_deleted=False)

    levels = query.filter_by(course_id=course_id).all()

    return flask.jsonify({
        'items': rod.model.schemas.LevelSchema(many=True).dump(levels).data,
        'meta': {'count': len(levels)}
    })


@course_handler.route('/course/<int:course_id>/level/<int:level_id>', methods=['PUT'])
def save_level(course_id, level_id):
    level = rod.model.schemas.LevelSchema().load(flask.request.json).data
    level.id = level_id

    rod.model.db.session.merge(level)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.LevelSchema().dump(level).data)
