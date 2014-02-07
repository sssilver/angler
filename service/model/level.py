from database import Base

from sqlalchemy.types import Integer, String

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import validates, relationship


class Level(Base):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
