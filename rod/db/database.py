from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session


class Database(object):
    def __init__(self, data_source):
        self.engine = create_engine(data_source, convert_unicode=True)

        self.session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                class_=NoDeleteSession
            )
        )

class NoDeleteSession(Session):
    def delete(self, instance):
        '''
        Do not actually delete the instance. Set the is_deleted flag instead.
        '''
        instance.is_deleted = True