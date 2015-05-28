import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.db
import rod.model.group


level_staff_table = sqlalchemy.schema.Table('level_staff', rod.db.Base.metadata,
    sqlalchemy.schema.Column('level_id', sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('level.id')),
    sqlalchemy.schema.Column('staff_id', sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('staff.id'))
)


class Level(rod.db.Base, rod.db.PersistentMixin):
    __tablename__ = 'level'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.String())

    # Course this level belongs to
    course_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('course.id'))
    course = sqlalchemy.orm.relationship(
        'Course',
        primaryjoin='and_(Level.course_id==Course.id)'
    )

    # Teachers who can teach this level
    teachers = sqlalchemy.orm.relationship(
        'Staff',
        secondary=level_staff_table,
        join_depth=30  # Up to the level's teachers
    )

    groups = sqlalchemy.orm.relationship(
        'Group',
        primaryjoin='and_(Level.id==Group.level_id)',
        back_populates='level'
    )
