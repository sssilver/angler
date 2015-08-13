import rod.handler.base
import rod.handler.rest
import rod.model.student


class StudentHandler(rod.handler.base.BaseHandler,
                     rod.handler.rest.Get,
                     rod.handler.rest.Put,
                     rod.handler.rest.Post,
                     rod.handler.rest.Delete):
    def initialize(self):
        self.resource = rod.model.student.Student

        super(StudentHandler, self).initialize()


def test(email, password):
    return [1, 2, 3]
