""" Module for all events related to log in/out. """
import json
import time
from functools import wraps
from http import HTTPStatus
from uuid import uuid4

import eventlet
from flask_socketio import emit
from global_context import PLAYERS
from objects.player import Player
from world.coordinates import Coordinate

from server import HttpError, app, socketio
from server.user import User


def login_required(f):
    @wraps(f)
    def log_in(*args, **kwargs):
        try:
            message = args[0]
        except IndexError:
            raise UnauthorizedError("Users must log in to access this!")

        try:
            user = User.retrieve(message["id"])
        except KeyError:
            raise UnauthorizedError("Users must log in to access this!")

        return f(user, *args, **kwargs)

    return log_in


class UnauthorizedError(HttpError):
    response_code = HTTPStatus.UNAUTHORIZED


@app.route("/health")
def health():
    print("Health checked")
    return {"status": "okay"}


@app.route("/test", methods=["POST"])
def test_post():
    print("post received")

    return {"hello": "world"}


@socketio.on("login")
def socket_login(message):

    print(f"Login requested: {message}")
    try:
        player_name = message["name"]
    except KeyError:
        raise UnauthorizedError("A username must be provided to log in")

    # TODO: Handle authentication

    # Give user a unique id to track which player they control
    user = User(player_name)

    user.store(user.id)

    emit("login_accepted", user)


@socketio.on("player_load")
@login_required
def load_player(user, message):
    # TODO: Handle authentication

    print("Loading player")

    for player in PLAYERS.values():
        emit("player_joined", player.json)

    user_id = user.id

    if user_id in PLAYERS:
        player = PLAYERS[user_id]
        print("Existing player loaded")
    else:
        player = Player.create(user.name)
        PLAYERS[user_id] = player

        player.position = Coordinate(-4, 1, 3)
        print("New player created")

    emit("player_load", player.json)
    emit("player_joined", player.json, broadcast=True, include_self=False)


@socketio.on("logout")
@login_required
def logout(user, message):

    print(f"Player logging out: {message}")
    if not isinstance(message, dict):
        message = json.loads(message)

    player = PLAYERS.pop(user.id)
    emit("player_logout", player.json, broadcast=True)

    player.store(player.uuid)


@socketio.on("check_in")
@login_required
def check_in(user, message):

    user.ping()
    print(f"{user.last_seen}: {user.name} checked in")


@socketio.on("connect")
def test_connect():
    """ Handle new socket connections. """

    print("Client connecting!")


@socketio.on("disconnect")
def test_disconnect():
    """ Handle sockets being disconnected. """

    print("Client disconnected")


def monitor_players():
    with app.app_context():
        while True:
            for user_id in list(PLAYERS.keys()):
                user = User.retrieve(user_id)
                if time.time() - user.last_seen > 30:
                    player = PLAYERS.pop(user_id)

                    print(f"Logging out {player}")

                    emit("player_logout", player.json, broadcast=True)

                    user.store(user.id)
                    player.store(player.uuid)

            eventlet.sleep(5)


eventlet.spawn(monitor_players)
