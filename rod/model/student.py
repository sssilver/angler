from datetime import datetime
import re
from sqlalchemy.types import String, Text
from sqlalchemy.types import Integer, SmallInteger
from sqlalchemy.types import Date, DateTime
from sqlalchemy.types import Boolean
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import select, func

from rod.db.base import PersistentMixin, Base
from rod.model.transaction import StudentTransaction
from rod.model.level import Level
from rod.model.comment import Comment
from rod.model.tariff import Tariff


class Student(PersistentMixin, Base):
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
    ivw_teacher_id = Column(Integer, ForeignKey('staff.id'))
    ivw_teacher = relationship(
        'Staff',
        primaryjoin='and_(Student.ivw_teacher_id==Staff.id)'
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

    transactions = relationship(
        'StudentTransaction',
        primaryjoin='and_(Student.id==StudentTransaction.student_id)',
        back_populates='student'
    )

    # Groups this student is a member of
    groups = relationship(
        'Group',
        secondary='student_group'
    )

    @hybrid_property
    def balance(self):
        return sum([transaction.amount for transaction in self.transactions])

    @balance.expression
    def balance(cls):
        return select([
            func.sum(StudentTransaction.amount)
        ]).where(StudentTransaction.student_id==cls.id).as_scalar()


    @validates('dob', 'reg_date', 'ivw_date')
    def validate_datetime(self, key, date):
        assert isinstance(date, datetime) or date is None
        return date

    @validates('email')
    def validate_email(self, key, email):
        assert re.match(r'[^@]+@[^@]+\.[^@]+', email)
        return email


class StudentGroup(PersistentMixin, Base):
    __tablename__ = 'student_group'

    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    student = relationship('Student')

    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)
    group = relationship('Group')

    tariff_id = Column(Integer, ForeignKey('tariff.id'))
    tariff = relationship('Tariff')

    # Date when student was added to the group
    add_date = Column(DateTime, default=datetime.utcnow)

    # Is the student's membership in this group suspended?
    # If yes, his balance will not be affected by absenteeism
    is_suspended = Column(Boolean)


class Attendance(PersistentMixin, Base):
    __tablename__ = 'attendance'

    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    student = relationship('Student')

    lesson_id = Column(Integer, ForeignKey('lesson.id'), primary_key=True)
    lesson = relationship('Lesson')

    # Was the student present(False) or absent(True)?
    is_absent = Column(Boolean)

    # TODO: Maybe add a note for this particular Student on this Lesson?
    #       Could also include the time at which the student showed up


class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student')
    day = Column(SmallInteger)  # 0..6 for each weekday
    range_from = Column(Integer)
    range_to = Column(Integer)
