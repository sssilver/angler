from datetime import datetime
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Enum
from sqlalchemy.types import DateTime
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship

from rod.db.base import PersistentBase


class Transaction(PersistentBase):
    __tablename__ = 'transaction'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)

    # Who paid? This depends on whether the Transaction is a
    # CompanyTransaction or a StudentTransaction. We use
    # SQLAlchemy's Single Table Inheritance to make this work.
    discriminator = Column('origin', String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    # When?
    time = Column(DateTime, default=datetime.utcnow)

    # Who administered it?
    staff_id = Column(Integer, ForeignKey('staff.id'))
    staff = relationship(
        'Staff',
        primaryjoin='and_(Transaction.staff_id==Staff.id)'
    )

    # How much? (includes the decimal part)
    amount = Column(Integer)  # Negative for refunds and lessons

    # Type of transaction
    type = Column(Enum(
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
        'refund_online_other'
    ))


class CompanyTransaction(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'company'}

    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship(
        'Company',
        primaryjoin='and_(CompanyTransaction.company_id==Company.id)'
    )


class StudentTransaction(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'student'}

    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship(
        'Student',
        primaryjoin='and_(StudentTransaction.student_id==Student.id)'
    )
