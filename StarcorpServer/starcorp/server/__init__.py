""" Package for containing server setup and logic. """
# pylint: disable=wrong-import-position

import os

import flask
from flask import Flask
from flask_socketio import SocketIO

from data.json_util import TYPE_META, Decoder, Encoder, Serializable

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

socketio.init_app(app, json=flask.json)


# Core imports
from .exceptions import *

# Set up events
from .login import *
from .player_input import *
from .data_requests import *
