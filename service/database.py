from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from db.session import ScoolSession



db_engine = create_engine('sqlite:///scool.db', convert_unicode=True)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
        class_=ScoolSession
    )
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # Import all models
    import model

    # Create their schemas in the database
    Base.metadata.create_all(bind=db_engine)
