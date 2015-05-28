import sqlalchemy.schema
import sqlalchemy.types

import rod.db


class Company(rod.db.Base, rod.db.PersistentMixin):
    __tablename__ = 'company'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.Text)

    # Contact person
    contact_name = sqlalchemy.schema.Column(sqlalchemy.types.Text)
    contact_email = sqlalchemy.schema.Column(sqlalchemy.types.Text)
    contact_phone = sqlalchemy.schema.Column(sqlalchemy.types.Text)
    contact_position = sqlalchemy.schema.Column(sqlalchemy.types.Text)
