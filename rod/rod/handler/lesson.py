import flask
import decimal
import dateutil.parser
import flask.ext.login

import rod
import rod.model.student
import rod.model.lesson
import rod.model.group
import rod.model.company
import rod.model.transaction
import rod.model.schemas


lesson_handler = flask.Blueprint('lesson', __name__)


@lesson_handler.route('/lesson', methods=['GET'])
def list_lesson():
    teacher_id = flask.request.args.get('teacher_id')

    query = rod.model.lesson.Lesson.query.filter_by(is_deleted=False)

    if teacher_id:
        lessons = query.filter_by(teacher_id=teacher_id).all()
    else:
        lessons = query.all()

    return flask.jsonify({
        'items': rod.model.schemas.LessonSchema(many=True).dump(lessons).data,
        'count': len(lessons)
    })


@lesson_handler.route('/group/<int:group_id>/lessons', methods=['POST'])
def file_lesson(group_id):
    lesson_data = flask.request.json

    # File the lesson
    lesson = rod.model.lesson.Lesson()
    lesson.time = dateutil.parser.parse(lesson_data['datetime'])
    lesson.teacher_id = flask.ext.login.current_user.id
    lesson.group_id = group_id
    rod.model.db.session.add(lesson)

    companies = set()  # Companies that had students in this lesson

    # Record attendance
    for student_id, is_absent in lesson_data['attendance'].iteritems():
        student_id = int(student_id)  # Cast to int, as JSON keys are always strings
        # Get each student
        student = rod.model.db.session.query(rod.model.student.Student).get(student_id)

        # Get their membership in this group
        membership_query = rod.model.db.session.query(rod.model.student.Membership)
        membership = membership_query.filter_by(student_id=student_id).filter_by(group_id=group_id).one()

        if membership.tariff.type == 'student':  # Student tariff?
            # For personal tariffs, we wanna update the student's balance
            student.balance -= membership.tariff.price

            student_transaction = rod.model.transaction.StudentTransaction()
            student_transaction.staff = lesson.teacher_id
            student_transaction.amount = membership.tariff.price
            student_transaction.student_id = student_id
            student_transaction.type = 'payment'

            rod.model.db.session.add(student_transaction)
        elif membership.tariff.type == 'company':  # Company tariff?
            # For corporate tariffs, we just wanna collect the companies that had students
            # in this lesson. We'll update their balances separately down the road.
            companies.add(membership.company)

    # Corporate balances are updated once,
    # regardless of how many students were in the group during this lesson
    for company in companies:
        # Update the corporate balance
        company.balance -= membership.tariff.price

        company_transaction = rod.model.transaction.CompanyTransaction()
        company_transaction.staff_id = lesson.teacher_id
        company_transaction.amount = membership.tariff.price
        company_transaction.company_id = company.id
        company_transaction.type = 'payment'

        rod.model.db.session.add(company_transaction)

    # Finally, commit the entire big transaction
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.LessonSchema().dump(lesson).data)
