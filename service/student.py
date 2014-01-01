from datetime import datetime
import re

from database import Base

from sqlalchemy.types import String
from sqlalchemy.types import Integer, SmallInteger
from sqlalchemy.types import Date, DateTime
from sqlalchemy.types import Boolean

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import validates, relationship


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)

    # Personal Information
    fname = Column(String(50))
    lname = Column(String(50))
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

    ivw_notes = Column(String)

    # Notes
    notes = Column(String)
    admin_notes = Column(String)
    teacher_notes = Column(String)
    previous_schools = Column(String)
    needs = Column(String)
    focus = Column(String)

    @validates('fname', 'lname')
    def validate_name(self, key, name):
        assert name.isalpha()
        return name

    @validates('dob', 'reg_date', 'ivw_date')
    def validate_datetime(self, key, date):
        return datetime.utcfromtimestamp(date)

    @validates('phone')
    def validate_name(self, key, phone):
        return phone

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


class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)


class Level(Base):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
