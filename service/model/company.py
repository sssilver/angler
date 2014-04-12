from database import Base

from sqlalchemy.types import Integer, String, Text

from sqlalchemy.schema import Column, ForeignKey


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    title = Column(Text)

    # Contact person
    contact_name = Column(Text)
    contact_phone = Column(Text)
    contact_position = Column(Text)