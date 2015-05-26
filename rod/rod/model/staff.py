import sqlalchemy.schema
import sqlalchemy.types

import rod.db



class Staff(rod.db.Base, rod.db.PersistentMixin):
    __tablename__ = 'staff'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)

    name = sqlalchemy.schema.Column(sqlalchemy.types.String)
    phone = sqlalchemy.schema.Column(sqlalchemy.types.String)
    email = sqlalchemy.schema.Column(sqlalchemy.types.String, unique=True)
    password = sqlalchemy.schema.Column(sqlalchemy.types.String)
    address = sqlalchemy.schema.Column(sqlalchemy.types.String)
    dob = sqlalchemy.schema.Column(sqlalchemy.types.Date)
    gender = sqlalchemy.schema.Column(sqlalchemy.types.Boolean)

    authenticated = sqlalchemy.schema.Column(sqlalchemy.types.Boolean, default=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        # TODO: Return the truth
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)