from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, exc, attributes, query
from sqlalchemy.orm.session import Session


class Database(object):
    def __init__(self, data_source):
        self.engine = create_engine(data_source, convert_unicode=True)

        self.session_class = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                class_=NoDeleteSession
            )
        )

        self.session = self.session_class

class NoDeleteSession(Session):
    def __init__(self, bind=None, autoflush=True, expire_on_commit=True,
                 _enable_transaction_accounting=True,
                 autocommit=False, twophase=False,
                 weak_identity_map=True, binds=None, extension=None,
                 info=None, query_cls=query.Query):

        self._persist_deleted = set()

        return super(NoDeleteSession, self).__init__(
            bind=bind,
            autoflush=autoflush,
            expire_on_commit=expire_on_commit,
            _enable_transaction_accounting=_enable_transaction_accounting,
            autocommit=autocommit,
            twophase=twophase,
            weak_identity_map=weak_identity_map,
            binds=binds,
            extension=extension,
            info=info,
            query_cls=query_cls
        )

    def delete(self, instance):
        '''
        Do not actually delete the instance. Set the is_deleted flag instead.
        '''
        instance.is_deleted = True
        self._persist_deleted.add(instance)


    @property
    def deleted(self):
        '''
        The set of all instances marked as deleted within this Session
        '''

        return self._persist_deleted
