from database import Base

from sqlalchemy.types import String
from sqlalchemy.types import Integer, SmallInteger
from sqlalchemy.types import Date, DateTime
from sqlalchemy.types import Boolean

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import validates, relationship


class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)

    # Personal Information
    fname = Column(String(50))
    lname = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    address = Column(String(100))
    dob = Column(Date)
    gender = Column(Boolean)


    @validates('fname', 'lname')
    def validate_name(self, key, name):
        assert name.isalpha()
        return name
