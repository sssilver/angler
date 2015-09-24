import sqlalchemy.schema
import sqlalchemy.types

import rod.model


class Company(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'company'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.Text)

    # Contact person
    contact_name = sqlalchemy.schema.Column(sqlalchemy.types.Text)
    contact_email = sqlalchemy.schema.Column(sqlalchemy.types.Text)
    contact_phone = sqlalchemy.schema.Column(sqlalchemy.types.Text)
    contact_position = sqlalchemy.schema.Column(sqlalchemy.types.Text)

    # Corporate balance
    balance = sqlalchemy.schema.Column(sqlalchemy.types.Numeric(scale=2), default=0.00)
