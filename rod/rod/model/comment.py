import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.model


class Comment(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'comment'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)

    # Staff the comment is posted by
    staff_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer,
                                        sqlalchemy.schema.ForeignKey(
                                            'staff.id',
                                            name='fk_comment_staff_id'
                                        ))
    staff = sqlalchemy.orm.relationship(
        'Staff'
    )

    # Student the comment refers to
    student_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer,
                                          sqlalchemy.schema.ForeignKey(
                                              'student.id',
                                              name='fk_comment_student_id'
                                          ))
    student = sqlalchemy.orm.relationship(
        'Student'
    )

    # Body of the comment
    body = sqlalchemy.schema.Column(sqlalchemy.types.Text)

    # Time posted
    time = sqlalchemy.schema.Column(sqlalchemy.types.DateTime)
