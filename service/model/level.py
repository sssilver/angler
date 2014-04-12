from database import Base

from sqlalchemy.types import Integer, String

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship

from course import Course


class Level(Base):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    # Course this level belongs to
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship(
        'Course',
        primaryjoin='and_(Level.course_id==Course.id)'
    )