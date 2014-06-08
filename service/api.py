from datetime import datetime

from cors import add_cors_headers

from model.staff import Staff
from model.course import Course
from model.level import Level
from model.tariff import Tariff
from model.student import Student, Availability
from model.company import Company
from model.transaction import StudentTransaction


def create_api_blueprints(manager):
    blueprints = []

    # Models to create blueprints for
    # TODO: Remove DELETE methods for models derived from PersistentBase
    models = [
        {
            'model': Staff,
            'methods': ['GET', 'PUT', 'PATCH', 'POST', 'DELETE']
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
            'preprocessors': {
                'POST': [pre_post_student]
            }
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
        }
    ]

    # Create the blueprints for each model with their respective options
    for model in models:
        blueprint = manager.create_api_blueprint(**model)
        blueprint.after_request(add_cors_headers)
        blueprints.append(blueprint)

    return blueprints


def pre_post_student(data):
    # Pop the availabilities data out of what came via HTTP
    availabilities_data = data.pop('availabilities')

    availability = []

    for day, ranges in enumerate(availabilities_data):
        for range in ranges:
            availability.append(Availability(**{
                'day': day,
                'range_from': int(range[0]),
                'range_to': int(range[1])
            }))

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

    data['availability'] = availability


def pre_post_transaction(data):
    data['time'] = str(datetime.utcnow())
    data['staff_id'] = 1  # TODO: Use the actual logged in staff data

    # Is this a refund? Then the amount has to be negative
    if data['type'].startswith('refund_'):
        data['amount'] = str(-1 * abs(int(data['amount'])))

        print data
