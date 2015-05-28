import rod.handler.base
import rod.handler.rest
import rod.model.course
import rod.db


class CourseHandler(rod.handler.base.BaseHandler,
                    rod.handler.rest.Get,
                    rod.handler.rest.Put,
                    rod.handler.rest.Post,
                    rod.handler.rest.Delete):

    def initialize(self):
        self.resource = rod.model.course.Course

        super(CourseHandler, self).initialize()
