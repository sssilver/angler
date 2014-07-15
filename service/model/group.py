from db.base import PersistentBase

from sqlalchemy.types import Integer, String

from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.orm import relationship


class Group(PersistentBase):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship(
        'Level',
        primaryjoin='and_(Level.id==Group.level_id)',
        back_populates='groups'
    )

    teacher_id = Column(Integer, ForeignKey('staff.id'))
    teacher = relationship(
        'Staff',
        primaryjoin='and_(Staff.id==Group.teacher_id)',
        back_populates='groups'
    )

    # Students who are a member of this group
    students = relationship(
        'Student',
        secondary='student_group',
        join_depth=30  # Up to the level's teachers
    )

