from db.base import PersistentBase

from flask.ext.login import UserMixin

from sqlalchemy.types import String
from sqlalchemy.types import Integer, SmallInteger
from sqlalchemy.types import Date, DateTime
from sqlalchemy.types import Boolean

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import validates, relationship


class Staff(PersistentBase, UserMixin):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True)

    # Personal Information
    name = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    address = Column(String(100))
    dob = Column(Date)
    gender = Column(Boolean)

    groups = relationship(
        'Group',
        primaryjoin='and_(Staff.id==Group.teacher_id)',
        back_populates='teacher'
    )