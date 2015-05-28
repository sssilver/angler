import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.db


class Lesson(rod.db.Base, rod.db.PersistentMixin):
    __tablename__ = 'lesson'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    date = sqlalchemy.schema.Column(sqlalchemy.types.DateTime)

    teacher_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('staff.id'))
    teacher = sqlalchemy.orm.relationship(
        'Staff',
        primaryjoin='and_(Staff.id==Lesson.teacher_id)',
        back_populates='lessons'
    )

    group_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('group.id'))
    group = sqlalchemy.orm.relationship(
        'Group',
        primaryjoin='and_(Group.id==Lesson.group_id)',
        back_populates='lessons'
    )

    # Students attendance for this lesson
    attendance = sqlalchemy.orm.relationship(
        'Attendance',
        primaryjoin='and_(Lesson.id==Attendance.lesson_id)',
        back_populates='lesson'
    )
