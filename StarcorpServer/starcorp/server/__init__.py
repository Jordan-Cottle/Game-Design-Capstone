from flask import Flask
from flask_socketio import SocketIO

# Set up server
app = Flask("StarCorp")
socketio = SocketIO(app)

# Set up events
from .login import *
from .movement import *