import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm

import rod.model


class Tariff(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'tariff'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.String())

    # Course this tariff belongs to
    course_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('course.id'))
    course = sqlalchemy.orm.relationship(
        'Course',
        back_populates='tariffs'
    )

    # Price of this payment plan
    price = sqlalchemy.schema.Column(sqlalchemy.types.Numeric(scale=2))

    # What type of a plan is this?
    type = sqlalchemy.schema.Column(sqlalchemy.types.Enum(
        'student',
        'company',

        name='tariff_type'
    ))
