""" Module for all events related to log in/out. """
import json
import time
from functools import wraps
from http import HTTPStatus

import eventlet
from database import DatabaseSession, create_user, get_user, login_user
from flask import request, session
from flask_socketio import disconnect, emit
from global_context import PLAYERS
from objects import Player, User
from server import HttpError, app, socketio
from utils import get_logger
from world import Coordinate

from server import HttpError, app, socketio

LOGGER = get_logger(__name__)

INACTIVE_TIMEOUT = 30


class UnauthorizedError(HttpError):
    """ Error for when an unauthorized access is attempted. """

    response_code = HTTPStatus.UNAUTHORIZED


class ProxyAccessError(Exception):
    """ Error for when access via a proxy object fails. """


class SessionProxy:
    """ Proxy object for accessing currently session context easily. """

    def __init__(self, name) -> None:
        self.name = name
        self.objects = {}

    def __getattr__(self, name):
        """ Route requests for attributes to the proxied object. """
        return getattr(self.value, name)

    @property
    def value(self):
        """ Get a reference to the proxied object. """
        try:
            return self.objects[session["session_id"]]
        except KeyError as error:
            raise ProxyAccessError(f"{self.name} proxy access failed") from error

    def push(self, obj):
        """ Add object to tracked objects. """

        LOGGER.debug(f"Setting {obj} into session {request.sid}")
        session["session_id"] = request.sid
        self.objects[request.sid] = obj

    def pop(self):
        """ Remove object from proxy stash. """
        return self.objects.pop(request.sid)

    def __enter__(self):
        """ Pass along context manager request to proxied object. """

        return self.value.__enter__()

    def __exit__(self, *args):
        """ Pass on context manager exit to proxied object. """

        return self.value.__exit__(*args)

    def __str__(self) -> str:
        try:
            return f"{self.value}"
        except ProxyAccessError:
            return f"{self.name} proxy with no value in current context"

    def __repr__(self) -> str:
        try:
            return f"{self.name} proxy: current={self.value}"
        except ProxyAccessError:
            return f"{self.name} proxy: current=None"


current_user = SessionProxy("user")
database_session = SessionProxy("database session")


@socketio.on_error()  # Handles the default namespace
def error_handler(error):
    """ Handle errors in socketio event handlers. """

    if isinstance(error, UnauthorizedError):
        LOGGER.exception(f"Unauthorized request detected during {request.event}")
        disconnect()
    else:
        LOGGER.exception(f"An unexpected {error!r} has ocurred during {request}!")
        disconnect()
        raise error


def login_required(func):
    """Decorator for enforcing a logged in user.

    Also pulls the token out of the request and passes a user instance into the decorated function.
    """

    @wraps(func)
    def check_log_in(*args, **kwargs):
        current_user.ping()

        return func(*args, **kwargs)

    return check_log_in


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
    # Push user into the proxy object for later reference
    current_user.push(user)

    LOGGER.info(f"{user} successfully logged in")
    emit("login_accepted", user)


@socketio.on("player_load")
@login_required
def load_player(message):  # pylint: disable=unused-argument
    """ Load a player into the world. """

    # TODO: Handle authentication

    LOGGER.info(f"Loading player for {current_user}")

    for player in PLAYERS.values():
        emit("player_joined", player.json)

    user_id = current_user.id

    if user_id in PLAYERS:
        player = PLAYERS[user_id]
        LOGGER.debug(f"Existing player loaded for {current_user}")
    else:
        player = Player.create(current_user.name, current_user.value)

        player.position = Coordinate(-4, 1, 3)
        LOGGER.info(f"New player created for {current_user}")

    emit("player_load", player.json)
    emit("player_joined", player.json, broadcast=True, include_self=False)


@socketio.on("logout")
@login_required
def logout(message):
    """ Process logout of a player. """

    LOGGER.info(f"Player logging out: {message}")
    if not isinstance(message, dict):
        message = json.loads(message)

    player = PLAYERS.pop(current_user.id)
    emit("player_logout", player.json, broadcast=True)

    player.store(player.uuid)


@socketio.on("check_in")
@login_required
def check_in(message):  # pylint: disable=unused-argument
    """ Update last seen time for a player. """

    current_user.ping()
    LOGGER.debug(f"{current_user.last_seen}: {current_user.name} checked in")


@socketio.on("connect")
def on_connect():
    """ Handle new socket connections. """

    LOGGER.debug("Client connecting!")
    database_session.push(DatabaseSession())


@socketio.on("disconnect")
def on_disconnect():
    """ Handle sockets being disconnected. """

    try:
        player = PLAYERS.pop(current_user.id)
    except ProxyAccessError:
        LOGGER.debug("Disconnecting client that failed to log in.")
    else:
        emit("player_logout", player.json, broadcast=True)
        player.store(player.uuid)
        LOGGER.debug(f"{current_user} disconnected")
        current_user.pop()

    database_session.close()
    database_session.pop()


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
