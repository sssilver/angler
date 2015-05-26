import datetime
import simplejson


class JSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()

        try:
            return obj.__json__()
        except AttributeError:
            return simplejson.JSONEncoder.default(self, obj)
