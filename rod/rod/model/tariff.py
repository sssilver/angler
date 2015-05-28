import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.db


class Tariff(rod.db.Base, rod.db.PersistentMixin):
    __tablename__ = 'tariff'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.String())

    # Course this tariff belongs to
    course_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('course.id'))
    course = sqlalchemy.orm.relationship(
        'Course',
        primaryjoin='and_(Tariff.course_id==Course.id)',
        back_populates='tariffs'
    )

    # Price of this payment plan
    price = sqlalchemy.schema.Column(sqlalchemy.types.Integer)

    # What type of a plan is this?
    type = sqlalchemy.schema.Column(sqlalchemy.types.Enum(
        'student',
        'company',

        name='tariff_type'
    ))
