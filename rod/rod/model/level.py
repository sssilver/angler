import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.model


class Level(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'level'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.String())

    # Course this level belongs to
    course_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('course.id'))
    course = sqlalchemy.orm.relationship(
        'Course'
    )

    groups = sqlalchemy.orm.relationship(
        'Group',
        back_populates='level'
    )
