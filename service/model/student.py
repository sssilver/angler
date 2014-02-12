from datetime import datetime
import re

from database import Base

from sqlalchemy.types import String
from sqlalchemy.types import Integer, SmallInteger
from sqlalchemy.types import Date, DateTime
from sqlalchemy.types import Boolean

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import validates, relationship

from staff import Teacher
from level import Level


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)

    # Personal Information
    name = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    address = Column(String(100))
    dob = Column(Date)
    gender = Column(Boolean)

    # Student Data
    reg_date = Column(DateTime, default=datetime.utcnow)
    ref_type = Column(Integer)
    ref = Column(String)

    # Availability
    availability = relationship(
        'Availability',
        primaryjoin='and_(Student.id==Availability.student_id)',
        back_populates='student'
    )

    # Interview
    ivw_date = Column(DateTime)
    ivw_teacher_id = Column(Integer, ForeignKey('teacher.id'))
    ivw_teacher = relationship(
        'Teacher',
        primaryjoin='and_(Student.ivw_teacher_id==Teacher.id)'
    )

    ivw_level_id = Column(Integer, ForeignKey('level.id'))
    ivw_level = relationship(
        'Level',
        primaryjoin='and_(Student.ivw_level_id==Level.id)'
    )

    ivw_notes = Column(Text)

    # Notes & comments
    note = Column(String)

    comments = relationship(
        'Comment',
        primaryjoin='and_(Student.id==Comment.student_id)',
        back_populates='student'
    )

    previous_schools = Column(Text)
    needs = Column(Text)
    focus = Column(Text)

    def serialize(self):
        return {'a': 'b'}

    @validates('dob', 'reg_date', 'ivw_date')
    def validate_datetime(self, key, date):
        assert isinstance(date, datetime)
        return date

    @validates('email')
    def validate_name(self, key, email):
        assert re.match(r'[^@]+@[^@]+\.[^@]+', email)
        return email


class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student')
    day = Column(SmallInteger)  # 0..6 for each weekday
    range_from = Column(Integer)
    range_to = Column(Integer)