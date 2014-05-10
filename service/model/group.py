from db.base import PersistentBase

from sqlalchemy.types import Integer, String

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship



group_student_table = Table('group_student', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id')),
    Column('student_id', Integer, ForeignKey('student.id'))
)


class Group(PersistentBase):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    levels = relationship(
        'Level',
        primaryjoin='and_(Course.id==Level.course_id)',
        back_populates='course'
    )
