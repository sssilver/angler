import flask

import rod
import rod.model.course
import rod.model.schemas


course = flask.Blueprint('course', __name__)


@course.route('/course', methods=['GET'])
def list_course():
    all_courses = rod.model.course.Course.query.filter_by(is_deleted=False).all()

    return flask.jsonify({
        'items': rod.model.schemas.CourseSchema(many=True).dump(all_courses).data,
        'count': len(all_courses)
    })


@course.route('/course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course_obj = rod.model.db.session.query(rod.model.course.Course).get(course_id)

    return flask.jsonify(rod.model.schemas.CourseSchema().dump(course_obj).data)


@course.route('/course', methods=['POST'])
def add_course():
    course_obj = rod.model.schemas.CourseSchema().load(flask.request.json).data
    rod.model.db.session.add(course_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.CourseSchema().dump(course_obj).data)


@course.route('/course/<int:course_id>', methods=['PUT'])
def save_course(course_id):
    course_obj = rod.model.schemas.CourseSchema().load(flask.request.json).data
    course_obj.id = course_id

    rod.model.db.session.merge(course_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.CourseSchema().dump(course_obj).data)


@course.route('/course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course_obj = rod.model.course.Course.query.get(course_id)

    rod.model.db.session.delete(course_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(course_obj).data)
