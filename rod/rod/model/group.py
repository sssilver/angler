import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.db


class Group(rod.db.Base, rod.db.PersistentMixin):
    __tablename__ = 'group'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.String(100))

    level_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('level.id'))
    level = sqlalchemy.orm.relationship(
        'Level',
        primaryjoin='and_(Level.id==Group.level_id)',
        back_populates='groups'
    )

    teacher_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('staff.id'))
    teacher = sqlalchemy.orm.relationship(
        'Staff',
        primaryjoin='and_(Staff.id==Group.teacher_id)',
        back_populates='groups'
    )

    # Students who are a member of this group
    students = sqlalchemy.orm.relationship(
        'StudentGroup'
    )

    # Lessons this group held
    lessons = sqlalchemy.orm.relationship(
        'Lesson',
        primaryjoin='and_(Group.id==Lesson.group_id)',
        back_populates='group'
    )
