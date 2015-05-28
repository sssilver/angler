import rod.handler.base
import rod.handler.rest
import rod.model.comment
import rod.db


class CommentHandler(rod.handler.base.BaseHandler,
                   rod.handler.rest.Get,
                   rod.handler.rest.Put,
                   rod.handler.rest.Post,
                   rod.handler.rest.Delete):

    def initialize(self):
        self.resource = rod.model.comment.Comment

        super(CommentHandler, self).initialize()
