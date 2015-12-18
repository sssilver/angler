import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.model


class Lesson(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'lesson'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    time = sqlalchemy.schema.Column(sqlalchemy.types.DateTime)

    teacher_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer,
                                          sqlalchemy.schema.ForeignKey(
                                              'staff.id',
                                              name='fk_lesson_teacher_id'
                                          ))
    teacher = sqlalchemy.orm.relationship(
        'Staff',
        back_populates='lessons'
    )

    group_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer,
                                        sqlalchemy.schema.ForeignKey(
                                            'group.id',
                                            name='fk_lesson_group_id'
                                        ))
    group = sqlalchemy.orm.relationship(
        'Group',
        back_populates='lessons'
    )

    # Students attendance for this lesson
    attendance = sqlalchemy.orm.relationship(
        'Attendance',
        back_populates='lesson'
    )
