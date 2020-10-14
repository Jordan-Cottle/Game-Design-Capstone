""" Module for all events related to log in/out. """
import json
from uuid import uuid4

from flask_socketio import emit
from global_context import PLAYER_LIST, SESSIONS
from objects.player import Player

from server import socketio


@socketio.on("loginRequest")
def process_login(message):
    """ Handle players attempting to login. """

    if not isinstance(message, dict):
        message = json.loads(message)

    print(f"Login requested: {message}")

    player_name = message.get("name")

    # TODO: Handle authentication

    if player_name is None:
        emit("login_denied", "A username must be provided to log in")

    if player_name in PLAYER_LIST:
        player = PLAYER_LIST[player_name]
        print("Existing player retrieved")
    else:
        player = Player()
        player.name = player_name
        PLAYER_LIST[player_name] = player
        print("New player created")

    # Give user a unique id to track which player they control
    session_id = str(uuid4())
    SESSIONS[session_id] = player

    response = {"player": player.json, "session_id": session_id}
    emit("login_accepted", response)


@socketio.on("connect")
def test_connect():
    """ Handle new socket connections. """

    print("Client connecting!")


@socketio.on("disconnect")
def test_disconnect():
    """ Handle sockets being disconnected. """

    print("Client disconnected")
