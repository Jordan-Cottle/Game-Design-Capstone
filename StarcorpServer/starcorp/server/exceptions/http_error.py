""" Module for containing a base http error and handler for returning exceptions from views. """

from flask import make_response

from server import app


class HttpError(Exception):
    """ Base exception for returning error responses via exception. """

    response_code = 500

    def __init__(self, message, response_code=None):
        super().__init__(message)
        self.message = message
        if response_code is not None:
            self.response_code = response_code

    @property
    def response(self):
        """ Convert the exception into an api response. """
        return make_response({"message": self.message}, self.response_code)


@app.errorhandler(HttpError)
def handle_http_error(error):
    """ Translate the unhandled error into an appropriate api response. """
    return error.response
