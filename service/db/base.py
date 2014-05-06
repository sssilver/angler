from database import Base

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean



class PersistentBase(Base):
    __abstract__ = True

    # This is set to 1 when an instance of a model derived from this class
    # is deleted
    is_deleted = Column(Boolean, default=0)