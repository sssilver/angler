import datetime
import re

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, Date, Boolean
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import validates, relationship


Base = declarative_base()


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
    reg_date = Column(Date, default=datetime.now)
    ref_type = Column(Integer)
    ref = Column(String)

    # Availability
    availability = relationship(
        'Availability',
        primaryjoin='and_(Student.id==Availability.student_id)',
        back_populates='student'
    )

    # Interview
    ivw_teacher = relationship(
        'Teacher',
        primaryjoin='and_(Student.ivw_teacher==Teacher.id)'
    )
    ivw_level = relationship(
        'Level',
        primaryjoin='and_(Student.ivw_level==Level.id)'
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

    @validates('phone')
    def validate_name(self, key, phone):
        return phone

    @validates('email')
    def validate_name(self, key, email):
        assert re.match(r'[^@]+@[^@]+\.[^@]+', email)
        return email


class Availability(Base):
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student')
    from = Column(Integer)
    to = Column(Integer)
