import flask

import rod
import rod.model.student
import rod.model.schemas


student = flask.Blueprint('student', __name__)


@student.route('/student', methods=['GET'])
def list_student():
    course_id = flask.request.args.get('course_id')

    query = rod.model.student.Student.query.filter_by(is_deleted=False)

    if course_id:
        students = query.filter_by(course_id=course_id).all()
    else:
        students = query.all()

    return flask.jsonify({
        'items': rod.model.schemas.StudentSchema(many=True).dump(students).data,
        'count': len(students)
    })


@student.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student_obj = rod.model.db.session.query(rod.model.student.Student).get(student_id)

    return flask.jsonify(rod.model.schemas.StudentSchema().dump(student_obj).data)


@student.route('/student', methods=['POST'])
def add_student():
    student_obj = rod.model.schemas.StudentSchema().load(flask.request.json).data

    rod.model.db.session.add(student_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StudentSchema().dump(student_obj).data)


@student.route('/student/<int:student_id>', methods=['PUT'])
def save_student(student_id):
    student_obj = rod.model.schemas.StudentSchema().load(flask.request.json).data
    student_obj.id = student_id

    rod.model.db.session.merge(student_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StudentSchema().dump(student_obj).data)


@student.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student_obj = rod.model.student.Student.query.get(student_id)

    rod.model.db.session.delete(student_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(student_obj).data)
