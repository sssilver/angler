from rod.db.base import PersistentBase

from sqlalchemy.types import Integer, String, DateTime

from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.orm import relationship


class Lesson(PersistentBase):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    teacher_id = Column(Integer, ForeignKey('staff.id'))
    teacher = relationship(
        'Staff',
        primaryjoin='and_(Staff.id==Lesson.teacher_id)',
        back_populates='lessons'
    )

    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship(
        'Group',
        primaryjoin='and_(Group.id==Lesson.group_id)',
        back_populates='lessons'
    )

    # Students attendance for this lesson
    attendance = relationship(
        'Attendance',
        primaryjoin='and_(Lesson.id==Attendance.lesson_id)',
        back_populates='lesson'
    )
