from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean
from sqlalchemy.ext.declarative import declarative_base

from rod import app


Base = declarative_base()
Base.query = app.db.session.query_property()


class PersistentMixin(object):
    # This is set to True when an instance of a model
    # derived from this class is deleted
    is_deleted = Column(Boolean, default=False)


def init_db():
    # Import all models
    import model

    # Create their schemas in the database
    Base.metadata.create_all(bind=app.db.engine)


