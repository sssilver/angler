import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.model


class Group(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'group'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.String(100))

    level_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('level.id'))
    level = sqlalchemy.orm.relationship(
        'Level',
        back_populates='groups'
    )

    teacher_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('staff.id'))
    teacher = sqlalchemy.orm.relationship(
        'Staff',
        back_populates='groups'
    )

    # Students who are a member of this group
    students = sqlalchemy.orm.relationship(
        'StudentGroup'
    )

    # Lessons this group held
    lessons = sqlalchemy.orm.relationship(
        'Lesson',
        back_populates='group'
    )
