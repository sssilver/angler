from db.base import PersistentBase

from sqlalchemy.types import String
from sqlalchemy.types import Integer, SmallInteger
from sqlalchemy.types import Date, DateTime
from sqlalchemy.types import Boolean

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import validates, relationship


class Staff(PersistentBase):
    __tablename__ = 'staff'
    #__table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    # Personal Information
    name = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(50))
    address = Column(String(100))
    dob = Column(Date)
    gender = Column(Boolean)

    groups = relationship(
        'Group',
        primaryjoin='and_(Staff.id==Group.teacher_id)',
        back_populates='teacher'
    )

    lessons = relationship(
        'Lesson',
        primaryjoin='and_(Staff.id==Lesson.teacher_id)',
        back_populates='teacher'
    )

    #
    # Authorization functions
    #

    def is_authenticated(self):
        return True

    def is_active(self):
        return not(self.is_deleted)

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
