import rod.model
import rod.model.course
import rod.model.staff


class CourseSchema(rod.model.BaseSchema):
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.course.Course


class StaffSchema(rod.model.BaseSchema):
    # Inherit BaseSchema's options
    class Meta(rod.model.BaseSchema.Meta):
        model = rod.model.staff.Staff
