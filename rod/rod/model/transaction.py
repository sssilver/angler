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
    staff_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer,
                                        sqlalchemy.schema.ForeignKey(
                                            'staff.id',
                                            name='fk_transaction_staff_id'
                                        ))
    staff = sqlalchemy.orm.relationship('Staff')

    # How much?
    amount = sqlalchemy.schema.Column(sqlalchemy.types.Numeric(scale=2))

    # Type of transaction
    type = sqlalchemy.schema.Column(sqlalchemy.types.Enum(
        'credit',  # Can be negative, for typo/adjustment reasons
        'payment',  # Happens every time the student's group files a lesson
        'refund',  # Taken off company balance

        name='transaction_type'
    ))

    # Method of payment
    method = sqlalchemy.schema.Column(sqlalchemy.types.Enum(
        'cash',
        'card',
        'transfer',
        'online_arca',
        'online_idram',
        'online_other',

        name='transaction_method'
    ))


class CompanyTransaction(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'company'}

    company_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer,
                                          sqlalchemy.schema.ForeignKey(
                                              'company.id',
                                              name='fk_transaction_company_id'
                                          ))
    company = sqlalchemy.orm.relationship(
        'Company'
    )


class StudentTransaction(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'student'}

    student_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer,
                                          sqlalchemy.schema.ForeignKey(
                                              'student.id',
                                              name='fk_transaction_student_id'
                                          ))
    student = sqlalchemy.orm.relationship(
        'Student'
    )
