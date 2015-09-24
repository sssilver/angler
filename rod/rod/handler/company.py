import flask

import rod
import rod.model.company
import rod.model.schemas


company_handler = flask.Blueprint('company', __name__)


@company_handler.route('/company', methods=['GET'])
def list_company():
    course_id = flask.request.args.get('course_id')

    query = rod.model.company.Company.query.filter_by(is_deleted=False)

    if course_id:
        companys = query.filter_by(course_id=course_id).all()
    else:
        companys = query.all()

    return flask.jsonify({
        'items': rod.model.schemas.CompanySchema(many=True).dump(companys).data,
        'count': len(companys)
    })


@company_handler.route('/company/<int:company_id>', methods=['GET'])
def get_company(company_id):
    company_obj = rod.model.db.session.query(rod.model.company.Company).get(company_id)

    return flask.jsonify(rod.model.schemas.CompanySchema().dump(company_obj).data)


@company_handler.route('/company', methods=['POST'])
def add_company():
    company_obj = rod.model.schemas.CompanySchema().load(flask.request.json).data

    rod.model.db.session.add(company_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.CompanySchema().dump(company_obj).data)


@company_handler.route('/company/<int:company_id>', methods=['PUT'])
def save_company(company_id):
    company_obj = rod.model.schemas.CompanySchema().load(flask.request.json).data
    company_obj.id = company_id

    rod.model.db.session.merge(company_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.CompanySchema().dump(company_obj).data)


@company_handler.route('/company/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    company_obj = rod.model.company.Company.query.get(company_id)

    rod.model.db.session.delete(company_obj)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StaffSchema().dump(company_obj).data)
