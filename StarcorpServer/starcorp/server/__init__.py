import os

import flask
from data.json_util import TYPE_META, Decoder, Encoder, Serializable
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

# Set up server
app = Flask("StarCorp")


app.secret_key = os.environ["SECRET_KEY"]

app.json_encoder = Encoder
app.json_decoder = Decoder

_make_response = app.make_response


def convert_custom_object(obj):

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
