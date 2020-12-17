""" Package for containing server setup and logic. """
# pylint: disable=wrong-import-position

import logging
import os
from logging.handlers import RotatingFileHandler
from uuid import uuid4

import flask
from flask import Flask
from flask_socketio import SocketIO, disconnect

from data import CONFIG, TYPE_META, Decoder, Encoder, Serializable
from exceptions import HttpError, SocketIOEventError
from utils.logging import FORMATTER

socketio = SocketIO()

# Set up server
app = Flask("StarCorp")


app.secret_key = os.environ["SECRET_KEY"]

app.json_encoder = Encoder
app.json_decoder = Decoder

_make_response = app.make_response


def convert_custom_object(obj):
    """ Handle custom objects via the json module. """

    if not isinstance(obj, Serializable):
        return _make_response(obj)

    data = obj.json
    data.pop(TYPE_META)
    return _make_response(data)


app.make_response = convert_custom_object


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


LOGGER = logging.getLogger("socketio")
log_config = CONFIG.get("logging.socketio")
handler = RotatingFileHandler(**log_config["handler"])
handler.setFormatter(FORMATTER)
LOGGER.setLevel(log_config["level"])
LOGGER.addHandler(handler)
socketio.init_app(app, json=flask.json, logger=LOGGER)


# Set up events
from .login import *
from .player_input import *
from .data_requests import *

from .game_loop import main_loop
