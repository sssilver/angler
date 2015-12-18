import flask
import flask.ext.sqlalchemy
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.orm.session
import sqlalchemy.schema
import sqlalchemy.types
import marshmallow_sqlalchemy


class RodSQLAlchemy(flask.ext.sqlalchemy.SQLAlchemy):
    def __init__(self, metadata=None):
        super(RodSQLAlchemy, self).__init__(metadata=metadata)

    def create_session(self, options):
        final_options = dict(options)

        if 'bind' not in final_options:
            final_options['bind'] = db.engine

        if 'autocommit' not in final_options:
            final_options['autocommit'] = False

        if 'autoflush' not in final_options:
            final_options['autoflush'] = False

        self.final_options = final_options

        return NoDeleteSession(**final_options)

    def init_schema(self):
        self.create_all()


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


meta = sqlalchemy.MetaData()
db = RodSQLAlchemy(metadata=meta)


class BaseSchema(marshmallow_sqlalchemy.ModelSchema):
    class Meta:
        sqla_session = db.session
