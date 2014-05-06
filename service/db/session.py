from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError



class ScoolSession(Session):
    def delete(self, instance):
        if hasattr(instance, 'is_deleted'):
            instance.is_deleted = 1
            self.commit()
        else:
            return super(ScoolSession, self).delete(instance)

    def query(self, *entities, **kwargs):
        all_results = super(ScoolSession, self).query(*entities, **kwargs)

        try:
            # Is this a PersistentModel?
            return all_results.filter_by(is_deleted=0)

        except InvalidRequestError:
            # No, just return everything
            return all_results