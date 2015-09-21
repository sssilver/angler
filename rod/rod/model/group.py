import sqlalchemy.types
import sqlalchemy.schema
import sqlalchemy.orm
import sqlalchemy.ext.hybrid

import rod.model


class Group(rod.model.db.Model, rod.model.PersistentMixin):
    __tablename__ = 'group'

    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, primary_key=True)
    title = sqlalchemy.schema.Column(sqlalchemy.types.String(100))

    level_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('level.id'))
    level = sqlalchemy.orm.relationship(
        'Level',
        back_populates='groups'
    )

    teacher_id = sqlalchemy.schema.Column(sqlalchemy.types.Integer, sqlalchemy.schema.ForeignKey('staff.id'))
    teacher = sqlalchemy.orm.relationship(
        'Staff',
        back_populates='groups'
    )

    # Students who are a member of this group
    memberships = sqlalchemy.orm.relationship(
        'Membership'
    )

    @sqlalchemy.ext.hybrid.hybrid_property
    def active_memberships(self):
        return [
            membership
            for membership in self.memberships
            if membership.is_deleted is not True
        ]

    @sqlalchemy.ext.hybrid.hybrid_property
    def inactive_memberships(self):
        return [
            membership
            for membership in self.memberships
            if membership.is_deleted is True
        ]

    # Lessons this group held
    lessons = sqlalchemy.orm.relationship(
        'Lesson',
        back_populates='group'
    )
