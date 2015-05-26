import tornado.web
import tornado.escape

import rod.handler.base
import rod.model.staff


class LoginHandler(rod.handler.base.BaseHandler):
    def post(self):
        args = tornado.escape.json_decode(self.request.body.decode('utf-8'))

        registered_user = rod.model.staff.Staff.query.filter_by(
            email=args['email'],
            password=args['password']
        ).first()

        if registered_user is None:
            raise tornado.web.HTTPError(401)

        # We have matching credentials, log the user in
        self.set_secure_cookie('user', str(registered_user.id))

        self.write({'email': registered_user.email})
