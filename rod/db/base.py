from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean
from sqlalchemy.ext.declarative import declarative_base
from rod import app



Base = declarative_base()
Base.query = app.db.session.query_property()



class PersistentBase(Base):
    __abstract__ = True

    # This is set to 1 when an instance of a model
    # derived from this class is deleted
    is_deleted = Column(Boolean, default=0)


def init_db():
    # Import all models
    import model

    # Create their schemas in the database
    PersistentBase.metadata.create_all(bind=db_engine)
