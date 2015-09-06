import flask
import decimal
import dateutil.parser
import flask.ext.login

import rod
import rod.model.student
import rod.model.lesson
import rod.model.company
import rod.model.transaction
import rod.model.schemas


lesson_handler = flask.Blueprint('lesson', __name__)


@lesson_handler.route('/lesson', methods=['GET'])
def list_lesson():
    return '{}'

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



@lesson_handler.route('/lesson/<int:group_id>', methods=['POST'])
def file_lesson(group_id):
    lesson_data = flask.request.json

    # File the lesson
    lesson = rod.model.lesson.Lesson()
    lesson.time = dateutil.parser.parse(lesson_data['time'])
    lesson.teacher_id = flask.ext.login.current_user.id
    lesson.group_id = group_id

    # ...and register it on the user's balance
    student_obj = rod.model.db.session.query(rod.model.student.Student).get(student_id)
    student_obj.balance = decimal.Decimal(student_obj.balance or 0) + amount

    rod.model.db.session.add(transaction)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StudentTransactionSchema().dump(transaction).data)
