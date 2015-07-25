import rod.handler.base
import rod.handler.rest
import rod.model.tariff
import rod.db



class TariffHandler(rod.handler.base.BaseHandler,
                    rod.handler.rest.Get,
                    rod.handler.rest.Put,
                    rod.handler.rest.Post,
                    rod.handler.rest.Delete):

    def initialize(self):
        self.resource = rod.model.tariff.Tariff

        super(TariffHandler, self).initialize()
