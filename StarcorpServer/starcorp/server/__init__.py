from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

# Set up server
app = Flask("StarCorp")

socketio.init_app(app)

# Set up events
from .login import *
from .player_input import *