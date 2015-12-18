import sqlalchemy.schema
import sqlalchemy.types
import sqlalchemy.orm
import flask.ext.bcrypt

import rod.model


class Staff(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'staff'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)

    # Personal Information
    name = sqlalchemy.schema.Column(sqlalchemy.types.String)
    phone = sqlalchemy.schema.Column(sqlalchemy.types.String)
    email = sqlalchemy.schema.Column(sqlalchemy.types.String, unique=True)
    password = sqlalchemy.schema.Column(sqlalchemy.types.String)
    address = sqlalchemy.schema.Column(sqlalchemy.types.String)
    dob = sqlalchemy.schema.Column(sqlalchemy.types.Date)
    gender = sqlalchemy.schema.Column(sqlalchemy.types.Boolean)

    ROLES = ['ADMIN', 'DIRECTOR', 'TEACHER']

    role = sqlalchemy.schema.Column(sqlalchemy.types.Enum(*ROLES, name='staff_role'), default='TEACHER')

    authenticated = sqlalchemy.schema.Column(sqlalchemy.types.Boolean, default=False)

    groups = sqlalchemy.orm.relationship(
        'Group',
        back_populates='teacher'
    )

    lessons = sqlalchemy.orm.relationship(
        'Lesson',
        back_populates='teacher'
    )

    def set_password(self, password):
        self.password = flask.ext.bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        # TODO: Return the truth
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
