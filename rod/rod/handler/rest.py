import tornado.web
import simplejson

import rod.handler.base


class Get(tornado.web.RequestHandler):
    @rod.handler.base.auth
    def get(self, resource_id=None, field=None):
        try:
            if resource_id is None:
                response = self.resource.query.filter_by(is_deleted=False).all()

            else:
                record = self.resource.query.get(int(resource_id))

                if field is None:
                    response = record
                else:
                    response = {field: getattr(record, field)}

            self.db.session.commit()

        except Exception, e:
            self.db.session.rollback()

            self.send_error(500, message=e.message)

        self.write(response)


class Put(tornado.web.RequestHandler):
    @rod.handler.base.auth
    def put(self, resource_id, field=None):
        data = simplejson.loads(self.request.body)
        resource = self.resource.query.get(int(resource_id))

        for field, value in data.iteritems():
            setattr(resource, field, value)

        try:
            self.db.session.commit()

            self.write(resource)
        except Exception, e:
            self.db.session.rollback()

            self.send_error(400, message=e.message)


class Post(tornado.web.RequestHandler):
    @rod.handler.base.auth
    def post(self, resource_id=None, field=None):
        data = simplejson.loads(self.request.body)
        resource = self.resource()

        for field, value in data.iteritems():
            if isinstance(value, dict):
                for subkey, subvalue in value.iteritems():
                    setattr(resource, '{}_{}'.format(field, subkey), subvalue)
            else:
                setattr(resource, field, value)

        try:
            self.db.session.add(resource)
            self.db.session.flush()

            self.db.session.commit()

            self.write(resource)
        except Exception, e:
            self.db.session.rollback()

            self.send_error(400, message=e.message)



class Delete(tornado.web.RequestHandler):
    @rod.handler.base.auth
    def delete(self, resource_id=None, field=None):
        if resource_id:
            try:
                resource = self.resource.query.get(int(resource_id))

                self.db.session.delete(resource)

                self.db.session.commit()

            except Exception, e:
                self.db.session.rollback()

                self.send_error(500, message=e.message)

