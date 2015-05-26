import rod.handler.base
import rod.handler.rest
import rod.model.staff
import rod.db


class StaffHandler(rod.handler.base.BaseHandler,
                   rod.handler.rest.Get,
                   rod.handler.rest.Put,
                   rod.handler.rest.Post,
                   rod.handler.rest.Delete):

    def initialize(self):
        self.resource = rod.model.staff.Staff

        super(StaffHandler, self).initialize()
