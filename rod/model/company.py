from db.base import PersistentBase

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text


class Company(PersistentBase):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    title = Column(Text)

    # Contact person
    contact_name = Column(Text)
    contact_email = Column(Text)
    contact_phone = Column(Text)
    contact_position = Column(Text)