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
        resource = self.resource.query.filter(self.resource.id == int(resource_id))

        resource.update(simplejson.loads(self.request.body))

        self.db.session.commit()

        self.write(resource)


class Post(tornado.web.RequestHandler):
    @rod.handler.base.auth
    def post(self, resource_id):
        resource = self.resource()

        data = simplejson.loads(self.request.body)

        for field, value in data.iteritems():
            setattr(resource, field, value)

        self.db.session.add(resource)
        self.db.session.flush()

        self.db.session.commit()

        self.write(resource)
