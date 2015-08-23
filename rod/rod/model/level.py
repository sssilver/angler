import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.model
import rod.model.group
import rod.model.course



class Level(rod.model.db, rod.model.PersistentMixin):
    __tablename__ = 'level'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.String())

    # Course this level belongs to
    course_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('course.id'))
    course = sqlalchemy.orm.relationship(
        'Course',
        primaryjoin='and_(Level.course_id==Course.id)'
    )

    groups = sqlalchemy.orm.relationship(
        'Group',
        primaryjoin='and_(Level.id==Group.level_id)',
        back_populates='level'
    )
