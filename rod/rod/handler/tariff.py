import flask

import rod
import rod.model.tariff
import rod.model.schemas


tariff = flask.Blueprint('tariff', __name__)


@tariff.route('/tariff', methods=['GET'])
def list_tariff():
    all_tariffs = rod.model.tariff.Tariff.query.filter_by(is_deleted=False).all()

    return flask.jsonify({
        'items': rod.model.schemas.TariffSchema(many=True).dump(all_tariffs).data,
        'count': len(all_tariffs)
    })


@tariff.route('/tariff/<int:tariff_id>', methods=['GET'])
def get_tariff(tariff_id):
    tariff_obj = rod.model.db.session.query(rod.model.tariff.Tariff).get(tariff_id)

    return flask.jsonify(rod.model.schemas.TariffSchema().dump(tariff_obj).data)


@tariff.route('/tariff', methods=['POST'])
def add_tariff():
    tariff_obj = rod.model.schemas.TariffSchema().load(flask.request.json).data

    rod.model.db.session.add(tariff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.TariffSchema().dump(tariff_obj).data)


@tariff.route('/tariff/<int:tariff_id>', methods=['PUT'])
def save_tariff(tariff_id):
    tariff_obj = rod.model.schemas.TariffSchema().load(flask.request.json).data
    tariff_obj.id = tariff_id

    rod.model.db.session.merge(tariff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.TariffSchema().dump(tariff_obj).data)


@tariff.route('/tariff/<int:tariff_id>', methods=['DELETE'])
def delete_tariff(tariff_id):
    tariff_obj = rod.model.tariff.Tariff.query.get(tariff_id)

    rod.model.db.session.delete(tariff_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(tariff_obj).data)
