import tornado.web
import simplejson

import rod.handler.base


class Get(tornado.web.RequestHandler):
    @rod.handler.base.auth
    def get(self, resource_id=None):
        if resource_id is None:
            response = self.resource.query.all()

        else:
            response = self.resource.query.get(int(resource_id))

        self.write(response)


class Put(tornado.web.RequestHandler):
    @rod.handler.base.auth
    def put(self, resource_id):
        staff = self.resource.query.filter(self.resource.id == int(resource_id))

        staff.update(simplejson.loads(self.request.body))

        self.db.session.commit()
