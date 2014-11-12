from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean
from sqlalchemy.ext.declarative import declarative_base
from rod import app


class PersistentBase(object):
    # This is set to True when an instance of a model
    # derived from this class is deleted
    is_deleted = Column(Boolean, default=False)


def init_db():
    # Import all models
    import model

    # Create their schemas in the database
    PersistentBase.metadata.create_all(bind=db_engine)


Base = declarative_base(cls=PersistentBase)
Base.query = app.db.session.query_property()

