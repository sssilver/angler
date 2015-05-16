import flask.ext.restful
import flask.ext.restful.reqparse


class Student(flask.ext.restful.Resource):
    def get(self, student_id=None):

        return {'student_id': str(student_id)}


