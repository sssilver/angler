import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.db
import rod.model.level
import rod.model.tariff


class Course(rod.db.Base, rod.db.PersistentMixin):
    __tablename__ = 'course'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.String())

    levels = sqlalchemy.orm.relationship(
        'Level',
        primaryjoin='and_(Course.id==Level.course_id)',
        back_populates='course'
    )

    tariffs = sqlalchemy.orm.relationship(
        'Tariff',
        primaryjoin='and_(Course.id==Tariff.course_id)',
        back_populates='course'
    )
