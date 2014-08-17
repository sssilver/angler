from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.orm.session import Session


class Database:
    def __init__(self, data_source):
        self.engine = create_engine(data_source, convert_unicode=True)

        self.session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )
