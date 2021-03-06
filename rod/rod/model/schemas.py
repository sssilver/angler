import marshmallow.fields
import marshmallow_sqlalchemy

import rod.model
import rod.model.course
import rod.model.staff
import rod.model.tariff
import rod.model.level
import rod.model.student
import rod.model.company
import rod.model.group
import rod.model.lesson
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
        exclude = ('course',)

    course_id = marshmallow_sqlalchemy.field_for(rod.model.tariff.Tariff, 'course_id')


class LevelSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.level.Level

    course = marshmallow.fields.Nested(CourseSchema, dump_only=True)
    groups = marshmallow_sqlalchemy.field_for(rod.model.level.Level, 'groups', dump_only=True)
    course_id = marshmallow_sqlalchemy.field_for(rod.model.level.Level, 'course_id')


class StudentSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.student.Student

    groups = marshmallow_sqlalchemy.field_for(rod.model.student.Student, 'groups', dump_only=True)
    transactions = marshmallow_sqlalchemy.field_for(rod.model.student.Student, 'transactions', dump_only=True)
    availability = marshmallow_sqlalchemy.field_for(rod.model.student.Student, 'availability', dump_only=True)
    comments = marshmallow_sqlalchemy.field_for(rod.model.student.Student, 'comments', dump_only=True)


class CompanySchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.company.Company


class MembershipSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.student.Membership

    student = marshmallow.fields.Nested(StudentSchema, dump_only=True)


class GroupSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.group.Group

    level = marshmallow.fields.Nested(LevelSchema, dump_only=True)
    teacher = marshmallow.fields.Nested(StaffSchema, dump_only=True)
    lessons = marshmallow_sqlalchemy.field_for(rod.model.group.Group, 'lessons', dump_only=True)
    level_id = marshmallow_sqlalchemy.field_for(rod.model.group.Group, 'level_id')
    teacher_id = marshmallow_sqlalchemy.field_for(rod.model.group.Group, 'teacher_id')
    memberships = marshmallow.fields.Nested(MembershipSchema, dump_only=True, many=True)
    active_memberships = marshmallow.fields.Nested(MembershipSchema, dump_only=True, many=True)
    inactive_memberships = marshmallow.fields.Nested(MembershipSchema, dump_only=True, many=True)


class LessonSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.lesson.Lesson

    group = marshmallow.fields.Nested(GroupSchema, dump_only=True)
    group_id = marshmallow_sqlalchemy.field_for(rod.model.lesson.Lesson, 'group_id')


class StudentTransactionSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.transaction.StudentTransaction


class CompanyTransactionSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.transaction.CompanyTransaction
