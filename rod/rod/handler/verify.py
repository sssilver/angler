import tornado.web

import rod.handler.base
import rod.model.staff


class VerifyHandler(rod.handler.base.BaseHandler):
    @rod.handler.base.auth
    def get(self):
        pass
