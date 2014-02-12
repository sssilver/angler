from database import Base

from sqlalchemy.types import Integer, String

from sqlalchemy.schema import Column, ForeignKey


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)

    # Who paid?
    payer_type = Column(Integer)
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship(
        'Student',
        primaryjoin='and_(Payment.student_id==Student.id)'
    )

    # When?
    time = Column(DateTime, default=datetime.utcnow)

    # Who administered it?
    staff_id = Column(Integer, ForeignKey('staff.id'))
    staff = relationship(
        'Staff',
        primaryjoin='and_(Payment.staff_id==Staff.id)'
    )