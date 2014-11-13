from sqlalchemy.types import Integer, String
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship

from rod.db.base import PersistentMixin, Base


class Course(PersistentMixin, Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    levels = relationship(
        'Level',
        primaryjoin='and_(Course.id==Level.course_id)',
        back_populates='course'
    )

    tariffs = relationship(
        'Tariff',
        primaryjoin='and_(Course.id==Tariff.course_id)',
        back_populates='course'
    )
