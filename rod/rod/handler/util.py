import flask.ext.restful
import flask.ext.restful.reqparse

import rod.db


class Util(flask.ext.restful.Resource):
    def get(self):
        rod.db.init_db()

        return {'status': 'OK'}

