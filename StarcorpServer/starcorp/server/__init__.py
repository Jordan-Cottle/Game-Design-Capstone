import os

from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager, current_user
from functools import wraps

from data.json_util import Serializable, TYPE_META, Encoder, Decoder


socketio = SocketIO()
login_manager = LoginManager()

# Set up server
app = Flask("StarCorp")

login_manager.init_app(app)

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

socketio.init_app(app)


def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


# Core imports
from .exceptions import *

# Set up events
from .login import *
from .player_input import *