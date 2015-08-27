import datetime
import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.model


class Transaction(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'transaction'
    __table_args__ = {'sqlite_autoincrement': True}

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)

    # Who paid? This depends on whether the Transaction is a
    # CompanyTransaction or a StudentTransaction. We use
    # SQLAlchemy's Single Table Inheritance to make this work.
    discriminator = sqlalchemy.schema.Column('origin', sqlalchemy.types.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    # When?
    time = sqlalchemy.schema.Column(sqlalchemy.types.DateTime, default=datetime.datetime.utcnow)

    # Who administered it?
    staff_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('staff.id'))
    staff = sqlalchemy.orm.relationship(
        'Staff'
    )

    # How much? (includes the decimal part)
    amount = sqlalchemy.schema.Column(sqlalchemy.types.Integer)  # Negative for refunds and lessons

    # Type of transaction
    type = sqlalchemy.schema.Column(sqlalchemy.types.Enum(
        'lesson',

        'cash',
        'card',
        'transfer',
        'online_arca',
        'online_idram',
        'online_other',

        'refund_cash',
        'refund_card',
        'refund_transfer',
        'refund_online_arca',
        'refund_online_idram',
        'refund_online_other',

        name='transaction_type'
    ))


class CompanyTransaction(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'company'}

    company_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('company.id'))
    company = sqlalchemy.orm.relationship(
        'Company'
    )


class StudentTransaction(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'student'}

    student_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('student.id'))
    student = sqlalchemy.orm.relationship(
        'Student'
    )
