import flask

import rod
import rod.model.tariff
import rod.model.schemas


tariff_handler = flask.Blueprint('tariff', __name__)


@tariff_handler.route('/tariff', methods=['GET'])
def list_tariff():
    course_id = flask.request.args.get('course_id')

    query = rod.model.tariff.Tariff.query.filter_by(is_deleted=False)

    if course_id:
        tariffs = query.filter_by(course_id=course_id).all()
    else:
        tariffs = query.all()

    return flask.jsonify({
        'items': rod.model.schemas.TariffSchema(many=True).dump(tariffs).data,
        'count': len(tariffs)
    })


@tariff_handler.route('/tariff/<int:tariff_id>', methods=['GET'])
def get_tariff(tariff_id):
    tariff_obj = rod.model.db.session.query(rod.model.tariff.Tariff).get(tariff_id)

    return flask.jsonify(rod.model.schemas.TariffSchema().dump(tariff_obj).data)


@tariff_handler.route('/tariff', methods=['POST'])
def add_tariff():
    tariff_obj = rod.model.schemas.TariffSchema().load(flask.request.json).data

    rod.model.db.session.add(tariff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.TariffSchema().dump(tariff_obj).data)


@tariff_handler.route('/tariff/<int:tariff_id>', methods=['PUT'])
def save_tariff(tariff_id):
    tariff_obj = rod.model.schemas.TariffSchema().load(flask.request.json).data
    tariff_obj.id = tariff_id

    rod.model.db.session.merge(tariff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.TariffSchema().dump(tariff_obj).data)


@tariff_handler.route('/tariff/<int:tariff_id>', methods=['DELETE'])
def delete_tariff(tariff_id):
    tariff_obj = rod.model.tariff.Tariff.query.get(tariff_id)

    rod.model.db.session.delete(tariff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(tariff_obj).data)
