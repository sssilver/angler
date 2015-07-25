import rod.handler.base
import rod.handler.rest
import rod.model.level
import rod.db


class LevelHandler(rod.handler.base.BaseHandler,
                    rod.handler.rest.Get,
                    rod.handler.rest.Put,
                    rod.handler.rest.Post,
                    rod.handler.rest.Delete):

    def initialize(self):
        self.resource = rod.model.level.Level

        super(LevelHandler, self).initialize()
