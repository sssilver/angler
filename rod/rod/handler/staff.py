import simplejson

import rod.handler.base
import rod.model.staff
import rod.db


class StaffHandler(rod.handler.base.BaseHandler):
    def initialize(self):
        super(StaffHandler, self).initialize()

    @rod.handler.base.auth
    def get(self, staff_id=None):
        staffs = rod.model.staff.Staff.query.all()

        self.write(staffs)

    @rod.handler.base.auth
    def put(self, staff_id):
        staff = rod.model.staff.Staff.query.filter(rod.model.staff.Staff.id == int(staff_id))

        staff.update(simplejson.loads(self.request.body))

        self.db.session.commit()

    @rod.handler.base.auth
    def post(self):
        pass
