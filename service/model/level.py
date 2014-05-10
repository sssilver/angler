from db.base import PersistentBase

from sqlalchemy.types import Integer, String

from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from course import Course


level_staff_table = Table('level_staff', PersistentBase.metadata,
    Column('level_id', Integer, ForeignKey('level.id')),
    Column('staff_id', Integer, ForeignKey('staff.id'))
)


class Level(PersistentBase):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    # Course this level belongs to
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship(
        'Course',
        primaryjoin='and_(Level.course_id==Course.id)'
    )

    # Teachers who can teach this level
    teachers = relationship(
        'Staff',
        secondary=level_staff_table,
        join_depth=30  # Up to the level's teachers
    )