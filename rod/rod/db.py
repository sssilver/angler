import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.orm.session
import sqlalchemy.ext.declarative
import sqlalchemy.schema
import sqlalchemy.types


declarative_base = lambda cls: sqlalchemy.ext.declarative.declarative_base(cls=cls)


class Database(object):
    def __init__(self, data_source):
        self.engine = sqlalchemy.create_engine(data_source, convert_unicode=True)

        self.session_class = sqlalchemy.orm.scoped_session(
            sqlalchemy.orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                class_=NoDeleteSession
            )
        )

        self.session = self.session_class

        Base.query = self.session.query_property()


@declarative_base
class Base(object):
    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def __json__(self):
        return self.columnitems


class NoDeleteSession(sqlalchemy.orm.session.Session):
    def __init__(self, bind=None, autoflush=True, expire_on_commit=True,
                 _enable_transaction_accounting=True,
                 autocommit=False, twophase=False,
                 weak_identity_map=True, binds=None, extension=None,
                 info=None, query_cls=sqlalchemy.orm.query.Query):

        self._persist_deleted = set()

        super(NoDeleteSession, self).__init__(
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
        # Do not actually delete the instance. Set the is_deleted flag instead.
        instance.is_deleted = True
        self._persist_deleted.add(instance)

    @property
    def deleted(self):
        # The set of all instances marked as deleted within this Session

        return self._persist_deleted


class PersistentMixin(object):
    # This is set to True when an instance of a model
    # derived from this class is deleted
    is_deleted = sqlalchemy.schema.Column(sqlalchemy.types.Boolean, default=False)
