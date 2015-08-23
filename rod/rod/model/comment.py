import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.model


class Comment(rod.model.db, rod.model.PersistentMixin):
    __tablename__ = 'comment'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)

    # Staff the comment is posted by
    staff_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('staff.id'))
    staff = sqlalchemy.orm.relationship(
        'Staff',
        primaryjoin='and_(Comment.staff_id==Staff.id)'
    )

    # Student the comment refers to
    student_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('student.id'))
    student = sqlalchemy.orm.relationship(
        'Student',
        primaryjoin='and_(Comment.student_id==Student.id)'
    )

    # Body of the comment
    body = sqlalchemy.schema.Column(sqlalchemy.types.Text)

    # Time posted
    time = sqlalchemy.schema.Column(sqlalchemy.types.DateTime)
