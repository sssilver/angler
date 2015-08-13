import simplejson

import rod.handler.base


class PaymentHandler(rod.handler.base.CorsHandler):
    @rod.handler.base.auth
    def post(self, resource_id=None, field=None):
        data = simplejson.loads(self.request.body)


