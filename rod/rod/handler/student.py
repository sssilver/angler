import rod.handler.base


class StudentHandler(rod.handler.base.BaseHandler):
    def initialize(self):
        super(StudentHandler, self).initialize()

    @rod.handler.base.auth
    def get(self, student_id=None):
        self.write({'student_id': str(student_id)})
