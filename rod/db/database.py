from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.orm.session import Session


db_engine = create_engine('sqlite:///scool.db', convert_unicode=True)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
        class_=Session
    )
)