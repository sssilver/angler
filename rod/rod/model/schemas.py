import marshmallow_sqlalchemy

import rod.model
import rod.model.course
import rod.model.staff
import rod.model.tariff
import rod.model.level
import rod.model.student
import rod.model.group
import rod.model.transaction


class CourseSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.course.Course


class StaffSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.staff.Staff


class TariffSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.tariff.Tariff


class LevelSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.level.Level
        exclude = ['course']

    groups = marshmallow_sqlalchemy.field_for(rod.model.level.Level, 'groups', dump_only=True)
    course_id = marshmallow_sqlalchemy.field_for(rod.model.level.Level, 'course_id')


class StudentSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.student.Student


class GroupSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.group.Group
        exclude = ['level', 'teacher']

    lessons = marshmallow_sqlalchemy.field_for(rod.model.group.Group, 'lessons', dump_only=True)
    level_id = marshmallow_sqlalchemy.field_for(rod.model.group.Group, 'level_id')
    teacher_id = marshmallow_sqlalchemy.field_for(rod.model.group.Group, 'teacher_id')


class StudentTransactionSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.transaction.StudentTransaction


class CompanyTransactionSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.transaction.CompanyTransaction
