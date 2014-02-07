from datetime import datetime
import logging

from flask import Flask, jsonify, request
from api import create_api_blueprints

from database import db_session, init_db
from flask.ext.cors import cross_origin
from flask.ext.restless import APIManager

from model.student import Student, Availability
from model.level import Level

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_object('config')

manager = APIManager(app, session=db_session)

blueprints = create_api_blueprints(manager, [Level, Student])
for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.route('/init', methods=['GET'])
def init():
    init_db()
    return 'OK'

"""
@app.route('/students', methods=['PUT'])
@origin(origin='*', headers='Content-Type')
def students():
    data = dict(request.get_json())
    availabilities_data = data.pop('availabilities')

    availability = []

    for day, ranges in enumerate(availabilities_data):
        for range in ranges:
            availability.append(Availability(**{
                'day': day,
                'range_from': int(range[0]),
                'range_to': int(range[1])
            }))

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

    new_student = Student(**data)

    print new_student

    try:
        db_session.add(new_student)
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()

    return scool_jsonify(request.get_json())


@app.route('/levels', methods=['PUT'])
@origin(origin='*', headers='Content-Type')
def save_level():
    data = dict(request.get_json())
    new_level = Level(**data)

    try:
        db_session.add(new_level)
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()

    return jsonify(request.get_json())

@app.route('/levels', methods=['GET'])
@origin(origin='*', headers='Content-Type')
def list_levels():
    levels = db_session.query(Level).order_by(Level.title).all()

    return scool_jsonify(levels)
"""

if __name__ == '__main__':
    app.run()
