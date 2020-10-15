""" Module for all events related to log in/out. """
import json
import time
from uuid import uuid4

import eventlet
from flask_socketio import emit
from global_context import PLAYER_LIST, SESSIONS
from objects.player import Player
from world.coordinates import Coordinate

from server import socketio
from server.user import User


@socketio.on("login_request")
def process_login(message):
    """ Handle players attempting to login. """

    if not isinstance(message, dict):
        message = json.loads(message)

    print(f"Login requested: {message}")

    player_name = message.get("name")

    # TODO: Handle authentication

    if player_name is None:
        emit("login_denied", "A username must be provided to log in")

    # Give user a unique id to track which player they control
    user = User(player_name)
    SESSIONS[user.session_id] = user

    emit("login_accepted", {"session_id": user.session_id})


@socketio.on("player_load")
def load_player(message):

    if not isinstance(message, dict):
        message = json.loads(message)

    session_id = message["session_id"]

    player_name = SESSIONS[session_id].name

    # TODO: Handle authentication

    for player in PLAYER_LIST.values():
        emit("player_joined", player.json)

    if player_name in PLAYER_LIST:
        player = PLAYER_LIST[player_name]
        print("Existing player loaded")
    else:
        player = Player()
        player.name = player_name
        PLAYER_LIST[player_name] = player

        player.position = Coordinate(-4, 1, 3)
        print("New player created")

    emit("player_load", player.json)
    emit("player_joined", player.json, broadcast=True, include_self=False)


@socketio.on("logout")
def logout(message):

    print(f"Player logging out: {message}")
    if not isinstance(message, dict):
        message = json.loads(message)

    user = SESSIONS.pop(message["session_id"])
    player = PLAYER_LIST.pop(user.name)
    emit("player_logout", player.json, broadcast=True)

    # TODO: Persist player object


@socketio.on("check_in")
def check_in(message):
    session_id = message["session_id"]

    user = SESSIONS[session_id]
    user.ping()
    print(f"{user.last_seen}: {user.name} checked in")


@socketio.on("connect")
def test_connect():
    """ Handle new socket connections. """

    print("Client connecting!")


@socketio.on("disconnect")
def check_players():
    """ Handle sockets being disconnected. """

    print("Client disconnected")

    eventlet.sleep(2)

    for user in list(SESSIONS.values()):
        if time.time() - user.last_seen > 2:

            SESSIONS.pop(user.session_id)
            player = PLAYER_LIST.pop(user.name)

            print(f"Logging out {player}")

            emit("player_logout", player.json, broadcast=True)

            # TODO: persist user
            # TODO: persist player
