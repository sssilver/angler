from db.base import PersistentBase

from sqlalchemy.types import Integer, String, Enum

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship

from course import Course


class Tariff(PersistentBase):
    __tablename__ = 'tariff'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    # Course this tariff belongs to
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship(
        'Course',
        primaryjoin='and_(Tariff.course_id==Course.id)'
    )

    # Price of this payment plan
    price = Column(Integer)

    # What type of a plan is this?
    type = Column(Enum(
        'student',
        'company'
    ))