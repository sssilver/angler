from rod.db.base import PersistentBase

from sqlalchemy.types import Text
from sqlalchemy.types import DateTime
from sqlalchemy.types import Integer

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship


class Comment(PersistentBase):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)

    # Staff the comment is posted by
    staff_id = Column(Integer, ForeignKey('staff.id'))
    staff = relationship(
        'Staff',
        primaryjoin='and_(Comment.staff_id==Staff.id)'
    )

    # Student the comment refers to
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship(
        'Student',
        primaryjoin='and_(Comment.student_id==Student.id)'
    )

    # Body of the comment
    body = Column(Text)

    # Time posted
    time = Column(DateTime)
