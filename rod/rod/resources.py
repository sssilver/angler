import rod.handler.student


def register(api):
    api.add_resource(rod.handler.student.Student, '/student', '/student/<student_id>')
