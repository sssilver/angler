import rod.model
import rod.model.course
import rod.model.staff
import rod.model.tariff
import rod.model.level


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
