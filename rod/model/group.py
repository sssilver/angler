from sqlalchemy.types import Integer, String
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from rod.db.base import PersistentMixin, Base


class Group(PersistentMixin, Base):
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
        'StudentGroup'
    )

    # Lessons this group held
    lessons = relationship(
        'Lesson',
        primaryjoin='and_(Group.id==Lesson.group_id)',
        back_populates='group'
    )
