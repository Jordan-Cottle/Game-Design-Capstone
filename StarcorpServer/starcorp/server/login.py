""" Module for all events related to log in/out. """
import json
import time
from functools import wraps
from http import HTTPStatus

import eventlet
from flask_socketio import emit

from global_context import PLAYERS
from objects import Player, User
from server import HttpError, app, socketio
from utils import get_logger
from world import Coordinate


LOGGER = get_logger(__name__)

INACTIVE_TIMEOUT = 30


def login_required(func):
    """Decorator for enforcing a logged in user.

    Also pulls the token out of the request and passes a user instance into the decorated function.
    """

    @wraps(func)
    def log_in(*args, **kwargs):
        try:
            message = args[0]
        except IndexError as error:
            raise UnauthorizedError("Users must log in to access this!") from error

        try:
            user = User.retrieve(message["id"])
        except KeyError as error:
            raise UnauthorizedError("Users must log in to access this!") from error

        user.ping()

        return func(user, *args, **kwargs)

    return log_in


class UnauthorizedError(HttpError):
    """ Error for when an unauthorized access is attempted. """

    response_code = HTTPStatus.UNAUTHORIZED


@app.route("/health")
def health():
    """ Return "okay" to provide simple endpoint to validate server is up. """

    LOGGER.debug("Health checked")
    return {"status": "okay"}


@socketio.on("login")
def socket_login(message):
    """ Process login even from a player. """

    LOGGER.info(f"Login requested: {message}")
    try:
        player_name = message["name"]
    except KeyError as error:
        raise UnauthorizedError("A username must be provided to log in") from error

    # TODO: Handle authentication

    # Give user a unique id to track which player they control
    user = User(player_name)

    user.store(user.id)

    emit("login_accepted", user)


@socketio.on("player_load")
@login_required
def load_player(user, message):  # pylint: disable=unused-argument
    """ Load a player into the world. """

    # TODO: Handle authentication

    LOGGER.info(f"Loading player for {user}")

    for player in PLAYERS.values():
        emit("player_joined", player.json)

    user_id = user.id

    if user_id in PLAYERS:
        player = PLAYERS[user_id]
        LOGGER.debug("Existing player loaded")
    else:
        player = Player.create(user.name, user)

        player.position = Coordinate(-4, 1, 3)
        LOGGER.info("New player created")

    emit("player_load", player.json)
    emit("player_joined", player.json, broadcast=True, include_self=False)


@socketio.on("logout")
@login_required
def logout(user, message):
    """ Process logout of a player. """

    LOGGER.info(f"Player logging out: {message}")
    if not isinstance(message, dict):
        message = json.loads(message)

    player = PLAYERS.pop(user.id)
    emit("player_logout", player.json, broadcast=True)

    player.store(player.uuid)


@socketio.on("check_in")
@login_required
def check_in(user, message):  # pylint: disable=unused-argument
    """ Update last seen time for a player. """

    user.ping()
    LOGGER.debug(f"{user.last_seen}: {user.name} checked in")


@socketio.on("connect")
def test_connect():
    """ Handle new socket connections. """

    LOGGER.debug("Client connecting!")


@socketio.on("disconnect")
def test_disconnect():
    """ Handle sockets being disconnected. """

    LOGGER.debug("Client disconnected")


def monitor_players():
    """ Watch for players who haven't pinged the server in a while and log them out. """
    with app.app_context():
        while True:
            for user_id in list(PLAYERS.keys()):
                user = User.retrieve(user_id)
                if time.time() - user.last_seen > INACTIVE_TIMEOUT:
                    player = PLAYERS.pop(user_id)

                    LOGGER.info(f"Logging out {player} due to inactivity")

                    socketio.emit("player_logout", player.json)

                    user.store(user.id)
                    player.store(player.uuid)

            eventlet.sleep(5)


eventlet.spawn(monitor_players)
