import rod.handler.base
import rod.handler.rest
import rod.model.student


class StudentHandler(rod.handler.base.BaseHandler,
                     rod.handler.rest.Get):
    def initialize(self):
        self.resource = rod.model.student.Student

        super(StudentHandler, self).initialize()

    @rod.handler.base.auth
    def post(self):
        pass
