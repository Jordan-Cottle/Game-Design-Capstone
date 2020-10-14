""" Main entrypoint for the Starcorp server. """

import json
from uuid import uuid4

from flask import Flask
from flask_socketio import SocketIO, emit

from data.json_util import Serializable

app = Flask(__name__)
socketio = SocketIO(app)


class Player(Serializable):
    """ Represent a player. """

    count = 0

    def __init__(self, name):
        Player.count += 1

        self.name = name
        self.player_id = uuid4()

    @property
    def json(self):
        return json.dumps({key: str(value) for key, value in self.__dict__.items()})

    @staticmethod
    def load(data):
        player = Player(data["name"])
        player.player_id = data["player_id"]
        return player

    def __str__(self):
        return f"{self.name} {self.player_id}"


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
