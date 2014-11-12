import sys

from datetime import datetime

from cors import add_cors_headers

from flask.ext.login import current_user
import bcrypt

from rod.model.course import Course
from rod.model.level import Level
from rod.model.tariff import Tariff
from rod.model.student import Student, StudentGroup, Availability, Attendance
from rod.model.company import Company
from rod.model.transaction import StudentTransaction, CompanyTransaction
from rod.model.group import Group
from rod.model.staff import Staff
from rod.model.lesson import Lesson

from rod import app


def create_api_blueprints(manager):
    blueprints = []

    # Models to create blueprints for
    # TODO: Remove DELETE methods for models derived from PersistentBase
    models = [
        {
            'model': Staff,
            'methods': ['GET', 'PUT', 'PATCH', 'POST', 'DELETE'],
            'preprocessors': {
                'POST': [pre_post_staff],
                'PATCH_SINGLE': [pre_patch_staff]
            },
            'postprocessors': {
                'GET_SINGLE': [post_get_single_staff],
                'GET_MANY': [post_get_many_staff]
            },
            'allow_patch_many': False
        },
        {
            'model': Course,
            'methods': ['GET', 'PUT', 'PATCH', 'POST', 'DELETE']
        },
        {
            'model': Level,
            'methods': ['GET', 'PUT', 'PATCH', 'POST', 'DELETE']
        },
        {
            'model': Tariff,
            'methods': ['GET', 'PUT', 'PATCH', 'POST', 'DELETE']
        },
        {
            'model': Student,
            'methods': ['GET', 'PUT', 'PATCH', 'POST', 'DELETE'],
            #'preprocessors': {
            #    'POST': [pre_post_student]
            #},
            'allow_patch_many': True
        },
        {
            'model': Company,
            'methods': ['GET', 'PUT', 'PATCH', 'POST', 'DELETE'],
        },
        {
            'model': StudentTransaction,
            'collection_name': 'student-transaction',
            'methods': ['GET', 'PUT', 'PATCH', 'POST', 'DELETE'],
            'preprocessors': {
                'POST': [pre_post_transaction]
            }
        },
        {
            'model': Group,
            'methods': ['GET', 'PUT', 'PATCH', 'POST', 'DELETE']
        },
        {
            'model': StudentGroup,
            'methods': ['GET', 'POST', 'DELETE']
        },
        {
            'model': Lesson,
            'methods': ['GET', 'POST', 'DELETE'],
            'preprocessors': {
                'POST': [pre_post_lesson]
            },
            'postprocessors': {
                'POST': [post_post_lesson]
            }
        }
    ]

    # Create the blueprints for each model with their respective options
    for model in models:
        blueprint = manager.create_api_blueprint(**model)
        blueprint.after_request(add_cors_headers)
        blueprints.append(blueprint)

    return blueprints


def pre_post_staff(data):
    # Secure the password
    data['password'] = bcrypt.hashpw(data['password'], bcrypt.gensalt())


def pre_patch_staff(instance_id=None, data=None, **kw):
    try:
        data['password'] = bcrypt.hashpw(data['password'], bcrypt.gensalt())
    except KeyError:
        pass


def post_get_single_staff(result=None, **kw):
    del result['password']


def post_get_many_staff(result=None, search_params=None, **kw):
    for staff in result['objects']:
        del staff['password']


def pre_post_student(data):
    # Pop the availabilities data out of what came via HTTP
    """
    availabilities_data = data.pop('availabilities')

    availability = []

    for day, ranges in enumerate(availabilities_data):
        for range in ranges:
            availability.append(Availability(**{
                'day': day,
                'range_from': int(range[0]),
                'range_to': int(range[1])
            }))

    data['availability'] = availability
    """

    #
    # Format the dates properly
    #

    try:
        data['dob'] = datetime.utcfromtimestamp(data['dob'])
    except KeyError:
        pass

    try:
        data['reg_date'] = datetime.utcfromtimestamp(data['reg_date'])
    except KeyError:
        pass

    try:
        data['ivw_date'] = datetime.utcfromtimestamp(data['ivw_date'])
    except KeyError:
        pass


def pre_post_transaction(data):
    data['time'] = str(datetime.utcnow())
    data['staff_id'] = current_user.id

    # Is this a refund? Then the amount has to be negative
    if data['type'].startswith('refund_'):
        data['amount'] = str(-1 * abs(int(data['amount'])))


def pre_post_lesson(data):
    # Pop the attendance data out of what came via HTTP
    attendance_data = data.pop('attendance')

    attendance = []

    for student_id, is_absent in attendance_data.iteritems():
        attendance.append(Attendance(**{
            'student_id': student_id,
            'is_absent': bool(is_absent)
        }))

    data['attendance'] = attendance

    data['date'] = str(data['date'])  #datetime.utcfromtimestamp(data['date'])

    # Add logged in Staff data
    data['teacher_id'] = current_user.id  # Comes from flask-login

def post_post_lesson(result=None, **kw):
    if not result:
        return

    # Get each of the actual student objects
    for student_attendance in result['attendance']:
        student_group = StudentGroup.query.get((
            student_attendance['student_id'],
            result['group_id']
        ))

        # Withdraw balance
        cost = student_group.tariff.price

        # TODO: Deal with CompanyTransaction differently
        transaction = StudentTransaction(**{
            'staff_id': current_user.id,
            'amount': str(student_group.tariff.price),
            'type': 'lesson',
            'student_id': student_attendance['student_id']
        })

        # Add the transaction
        app.db.session.add(transaction)

    app.db.session.commit()


    return result
