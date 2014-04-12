from database import Base
from datetime import datetime

from sqlalchemy import UniqueConstraint

from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Enum
from sqlalchemy.types import DateTime

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship



class Transaction(Base):
    __tablename__ = 'transaction'

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

    # How much?
    amount = Column(Integer)  # Negative for refunds, includes the decimal part

    # Type of transaction
    type = Column(Enum(
        'cash',
        'card',
        'transfer',
        'online_arca',
        'online_idram',
        'online_other'
    ))


class CompanyTransaction(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'company'}

    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship(
        'Company',
        primaryjoin='and_(Transaction.company_id=Company.id)'
    )


class StudentTransaction(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'student'}

    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship(
        'Student',
        primaryjoin='and_(Transaction.student_id=Student.id)'
    )
