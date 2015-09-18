import datetime
import re
import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm
import sqlalchemy.ext.hybrid
import sqlalchemy.sql

import rod.model


class Student(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'student'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)

    # Personal Information
    name = sqlalchemy.schema.Column(sqlalchemy.types.String())
    phone = sqlalchemy.schema.Column(sqlalchemy.types.String())
    email = sqlalchemy.schema.Column(sqlalchemy.types.String())
    address = sqlalchemy.schema.Column(sqlalchemy.types.String())
    dob = sqlalchemy.schema.Column(sqlalchemy.types.Date)
    gender = sqlalchemy.schema.Column(sqlalchemy.types.Boolean)

    # Student Data
    reg_date = sqlalchemy.schema.Column(sqlalchemy.types.Date, default=datetime.datetime.utcnow)
    ref_type = sqlalchemy.schema.Column(sqlalchemy.types.Integer)
    ref = sqlalchemy.schema.Column(sqlalchemy.types.String())

    # Availability
    availability = sqlalchemy.orm.relationship(
        'Availability',
        back_populates='student'
    )

    # Interview
    ivw_date = sqlalchemy.schema.Column(sqlalchemy.types.Date)
    ivw_time = sqlalchemy.schema.Column(sqlalchemy.types.Time(timezone=True))
    ivw_teacher_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('staff.id'))
    ivw_teacher = sqlalchemy.orm.relationship(
        'Staff'
    )

    ivw_level_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('level.id'))
    ivw_level = sqlalchemy.orm.relationship(
        'Level'
    )

    ivw_notes = sqlalchemy.schema.Column(sqlalchemy.types.Text())

    # Notes & comments
    note = sqlalchemy.schema.Column(sqlalchemy.types.String())

    comments = sqlalchemy.orm.relationship(
        'Comment',
        back_populates='student'
    )

    previous_schools = sqlalchemy.schema.Column(sqlalchemy.types.Text())
    needs = sqlalchemy.schema.Column(sqlalchemy.types.Text())
    focus = sqlalchemy.schema.Column(sqlalchemy.types.Text())

    transactions = sqlalchemy.orm.relationship(
        'StudentTransaction',
        back_populates='student'
    )

    # Groups this student is a member of
    groups = sqlalchemy.orm.relationship(
        'Group',
        secondary='student_group'
    )

    # Student balance
    balance = sqlalchemy.schema.Column(sqlalchemy.types.Numeric(scale=2))

    '''
    @sqlalchemy.ext.hybrid.hybrid_property
    def balance(self):
        return sum([transaction.amount for transaction in self.transactions])

    @balance.expression
    def balance(cls):
        return sqlalchemy.sql.select([
            sqlalchemy.sql.func.sum(StudentTransaction.amount)
        ]).where(StudentTransaction.student_id==cls.id).as_scalar()
    '''

    @sqlalchemy.orm.validates('email')
    def validate_email(self, key, email):
        if email is None:
            return None

        assert re.match(r'[^@]+@[^@]+\.[^@]+', email)
        return email


class StudentGroup(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'student_group'

    student_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('student.id'), primary_key=True)
    student = sqlalchemy.orm.relationship('Student')

    group_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('group.id'), primary_key=True)
    group = sqlalchemy.orm.relationship('Group')

    tariff_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('tariff.id'))
    tariff = sqlalchemy.orm.relationship('Tariff')

    # Date when student was added to the group
    add_date = sqlalchemy.schema.Column(sqlalchemy.types.DateTime, default=datetime.datetime.utcnow)

    # Is the student's membership in this group suspended?
    # If yes, his balance will not be affected by absenteeism
    is_suspended = sqlalchemy.schema.Column(sqlalchemy.types.Boolean)


class Attendance(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'attendance'

    student_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('student.id'), primary_key=True)
    student = sqlalchemy.orm.relationship('Student')

    lesson_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('lesson.id'), primary_key=True)
    lesson = sqlalchemy.orm.relationship('Lesson')

    # Was the student present(False) or absent(True)?
    is_absent = sqlalchemy.schema.Column(sqlalchemy.types.Boolean)

    # TODO: Maybe add a note for this particular Student on this Lesson?
    #       Could also include the time at which the student showed up


class Availability(rod.model.db.Model):
    __tablename__ = 'availability'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    student_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('student.id'))
    student = sqlalchemy.orm.relationship('Student')
    day = sqlalchemy.schema.Column(sqlalchemy.types.SmallInteger)  # 0..6 for each weekday
    range_from = sqlalchemy.schema.Column(sqlalchemy.types.Integer)
    range_to = sqlalchemy.schema.Column(sqlalchemy.types.Integer)
