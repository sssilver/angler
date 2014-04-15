from database import Base

from sqlalchemy.types import Integer, String

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    levels = relationship(
        'Level',
        primaryjoin='and_(Course.id==Level.course_id)',
        back_populates='course'
    )
