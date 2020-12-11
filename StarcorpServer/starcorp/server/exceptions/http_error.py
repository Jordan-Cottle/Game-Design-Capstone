from flask import make_response

from server import app


class HttpError(Exception):
    response_code = 500

    def __init__(self, message, response_code=None):
        self.message = message
        if response_code != None:
            self.response_code = response_code

    @property
    def response(self):
        return make_response({"message": self.message}, self.response_code)


@app.errorhandler(HttpError)
def handle_http_error(error):
    return error.response
