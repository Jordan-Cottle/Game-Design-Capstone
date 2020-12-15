""" Module for containing a base http error and handler for returning exceptions from views. """
from uuid import uuid4
from flask import make_response, request
from flask_socketio import emit, disconnect

from server import app, socketio
from utils import get_logger

LOGGER = get_logger(__name__)


class HttpError(Exception):
    """ Base exception for returning error responses via exception. """

    response_code = 500

    def __init__(self, message, response_code=None):
        super().__init__(message)
        self.message = message
        self.id = uuid4()
        if response_code is not None:
            self.response_code = response_code

    @property
    def type(self):
        """ Get type of this error as a string. """

        return self.__class__.__qualname__

    @property
    def response(self):
        """ Convert the exception into an api response. """
        return make_response(
            {"reason": self.message, "error_id": self.id}, self.response_code
        )


class SocketIOEventError(Exception):
    """ Errors that should be handled by emitting an event to current socketio connection. """

    event = "error"

    def __init__(self, message, event=None):
        super().__init__(message)
        self.message = message
        self.id = uuid4()
        if event is not None:
            self.event = event

    @property
    def type(self):
        """ Get type of this error as a string. """

        return self.__class__.__qualname__

    @property
    def response(self):
        """ Convert exception into data for a response. """

        return {"reason": self.message, "error_id": str(self.id)}

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.type}(message={self.message}, event={self.event})<id={self.id}>"


@app.errorhandler(HttpError)
def handle_http_error(error):
    """ Translate the unhandled error into an appropriate api response. """
    return error.response


@socketio.on_error()
def handle_error(error):
    """ Handle generic SocketIOEventError. """

    if isinstance(error, SocketIOEventError):
        LOGGER.warning(f"Error encountered during {request.event}: {error!r}")
        emit(error.event, error.response)
    else:
        error_id = uuid4()
        LOGGER.exception(
            f"An unexpected {error!r} has ocurred during {request.event}. Error id: {error_id}!"
        )
        emit("error", {"reason": "An unexpected error ocurred", "id": str(error_id)})
        disconnect()
        raise error