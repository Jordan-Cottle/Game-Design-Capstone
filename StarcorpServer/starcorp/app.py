""" Main entrypoint for the Starcorp server. """

import json
from uuid import uuid4

from flask import Flask
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on("loginRequest")
def process_login(message):
    """ Handle players attempting to login. """

    if not isinstance(message, dict):
        message = json.loads(message)

    print(f"Login requested: {message}")
    emit("login", Player(message["data"]).json)


@socketio.on("connect")
def test_connect():
    """ Handle new socket connections. """

    print("Client connecting!")


@socketio.on("disconnect")
def test_disconnect():
    """ Handle sockets being disconnected. """

    print("Client disconnected")


if __name__ == "__main__":
    print("Starting server!")
    socketio.run(app, host="192.168.1.16", port="1234")
