import flask
import decimal
import flask.ext.login

import rod
import rod.model.student
import rod.model.company
import rod.model.transaction
import rod.model.schemas


credit_handler = flask.Blueprint('credit', __name__)


@credit_handler.route('/credit/student/<int:student_id>', methods=['POST'])
def student_credit(student_id):
    amount = decimal.Decimal(flask.request.json['amount'])

    # Add the credit transaction
    transaction = rod.model.transaction.StudentTransaction()
    transaction.student_id = student_id
    transaction.amount = amount
    transaction.type = 'credit'
    transaction.method = flask.request.json['method']
    transaction.staff_id = flask.ext.login.current_user.id

    # ...and register it on the user's balance
    student_obj = rod.model.db.session.query(rod.model.student.Student).get(student_id)
    student_obj.balance = decimal.Decimal(student_obj.balance or 0) + amount

    rod.model.db.session.add(transaction)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.StudentTransactionSchema().dump(transaction).data)


@credit_handler.route('/credit/company/<int:company_id>', methods=['POST'])
def company_credit(company_id):
    amount = decimal.Decimal(flask.request.json['amount'])

    # Add the credit transaction
    transaction = rod.model.transaction.CompanyTransaction()
    transaction.company_id = company_id
    transaction.amount = amount
    transaction.type = 'credit'
    transaction.method = flask.request.json['method']
    transaction.staff_id = flask.ext.login.current_user.id

    # ...and register it on the company's balance
    company_obj = rod.model.db.session.query(rod.model.company.Company).get(company_id)
    company_obj.balance += amount

    rod.model.db.session.add(transaction)
    rod.model.db.session.commit()

    return flask.jsonify(rod.model.schemas.CompanyTransactionSchema().dump(transaction).data)
