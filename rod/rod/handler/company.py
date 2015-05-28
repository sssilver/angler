import rod.handler.base
import rod.handler.rest
import rod.model.company
import rod.db


class CompanyHandler(rod.handler.base.BaseHandler,
                   rod.handler.rest.Get,
                   rod.handler.rest.Put,
                   rod.handler.rest.Post,
                   rod.handler.rest.Delete):

    def initialize(self):
        self.resource = rod.model.company.Company

        super(CompanyHandler, self).initialize()
