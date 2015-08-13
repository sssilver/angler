import werkzeug.utils
import werkzeug.wrappers
import werkzeug.contrib.wrappers
import werkzeug.exceptions
import simplejson


class JSONRequest(werkzeug.wrappers.BaseRequest):
    # Accept up to 8MB of transmitted data.
    max_content_length = 1024 * 1024 * 8

    @property
    def json(self):
        if not self.data:
            return {}

        try:
            return simplejson.loads(self.data)
        except simplejson.JSONDecodeError:
            raise werkzeug.exceptions.BadRequest('JSON decode error')


class JSONResponse(werkzeug.wrappers.BaseResponse):
    def __init__(self, json_data, headers=None):
        super(JSONResponse, self).__init__(
            response=simplejson.dumps(json_data),
            status=200,
            headers=headers,
            mimetype='application/json',
            content_type='application/json'
        )
