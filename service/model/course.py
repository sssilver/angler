from database import Base

from sqlalchemy.types import Integer, String

from sqlalchemy.schema import Column, ForeignKey


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
