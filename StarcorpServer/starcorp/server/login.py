""" Module for all events related to log in/out. """
import json
from datetime import datetime, timedelta
from functools import wraps

import eventlet
from data import CONFIG, ShipSystemAttributeType
from database import (
    DatabaseSession,
    create_user,
    login_user,
    create_ship,
    get_location,
    get_upgrade,
)
from flask import request, session
from flask_socketio import emit
from database.ship import get_chassis, get_ship_system
from database.world import get_sector
from global_context import PLAYERS
from utils import get_logger
from world import Coordinate

from server import app, socketio
from exceptions import SocketIOEventError

LOGGER = get_logger(__name__)

INACTIVE_TIMEOUT = 30


class UnauthorizedError(SocketIOEventError):
    """ Error for when an unauthorized access is attempted. """

    event = "unauthorized"


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

ACTIVE_PLAYERS = set()


def create_initial_ship():
    """ Create default ship for a player. """

    ship_config = CONFIG.get("game.players.default_ship")
    sector = get_sector(database_session, sector_name=ship_config["sector"])
    location = get_location(
        database_session, sector, Coordinate.load(ship_config["location"])
    )
    chassis = get_chassis(database_session, name=ship_config["chassis"])

    loadout = []
    for system_name in ship_config["loadout"]:
        system = get_ship_system(database_session, name=system_name)
        loadout.append(system)

    ship = create_ship(database_session, current_user, location, chassis, loadout)
    database_session.commit()
    return ship


def get_systems(ship):
    """ Get all the systems, and the next upgrades, for a ship. """

    systems = []
    for slot in ship.loadout:

        upgrade = get_upgrade(database_session, slot.system)
        if upgrade is not None:
            upgrade_cost = upgrade.get_attribute(ShipSystemAttributeType.BASE_COST)
        else:
            upgrade_cost = -1

        data = {
            "name": slot.system.name,
            "upgrade_cost": upgrade_cost,
        }
        attributes = []
        for attribute in slot.system.attributes:
            if upgrade is not None:
                upgraded_value = upgrade.get_attribute(attribute.type)
            else:
                upgraded_value = -1

            attr_data = {
                "name": attribute.type,
                "value": attribute.value,
                "upgraded_value": upgraded_value,
            }
            attributes.append(attr_data)

        data["attributes"] = attributes
        systems.append(data)

    return systems


def login_required(func):
    """Decorator for enforcing a logged in user.

    Also pulls the token out of the request and passes a user instance into the decorated function.
    """

    @wraps(func)
    def check_log_in(*args, **kwargs):
        current_user.ping()
        database_session.commit()

        return func(*args, **kwargs)

    return check_log_in


@app.route("/health")
def health():
    """ Return "okay" to provide simple endpoint to validate server is up. """

    LOGGER.debug("Health checked")
    return {"status": "okay"}


@socketio.on("register")
def register_user(message):
    """ Handle creating a new user in the database. """

    LOGGER.debug(f"Attempting to create user from {message}")
    try:
        user_name = message["user_name"]
        email = message["email"]
        password = message["password"]
    except KeyError as error:
        raise UnauthorizedError(
            "A username, email, and password must be provided to register"
        ) from error

    user = create_user(database_session, user_name, email, password)
    database_session.commit()

    LOGGER.info(f"New user registered: {user.email} as {user.name}")

    emit(
        "registration_success",
        {"user_id": user.id, "user_name": user.name, "email": user.email},
    )


@socketio.on("login")
def socket_login(message):
    """ Process login even from a player. """

    LOGGER.info(f"Login requested: {message}")
    try:
        email = message["email"]
        password = message["password"]
    except KeyError as error:
        raise UnauthorizedError(
            "A username and password must be provided to log in"
        ) from error

    user = login_user(database_session, email, password)

    # Push user into the proxy object for later reference
    current_user.push(user)

    LOGGER.info(f"{user} successfully logged in")
    emit("login_accepted", user)


@socketio.on("player_load")
@login_required
def load_player(message):  # pylint: disable=unused-argument
    """ Load a player into the world. """

    LOGGER.info(f"Loading ship for {current_user}")

    for player in ACTIVE_PLAYERS:
        emit(
            "player_joined",
            {"id": player.ship.id, "position": player.ship.location.coordinate},
        )

    assert (
        current_user.value not in ACTIVE_PLAYERS
    ), "Players shouldn't need to load twice"

    if current_user.ship is None:
        current_user.ship = create_initial_ship()

    ship = current_user.ship
    LOGGER.debug(f"Loaded current user ship: {ship}")

    ACTIVE_PLAYERS.add(current_user.value)

    ship_data = {"id": ship.id, "position": ship.location.coordinate}
    emit("player_joined", ship_data, broadcast=True, include_self=False)

    ship_data["systems"] = get_systems(ship)
    emit("player_load", ship_data)


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

    ACTIVE_PLAYERS.remove(current_user.value)


@socketio.on("connect")
def on_connect():
    """ Handle new socket connections. """

    LOGGER.debug("Client connecting!")
    database_session.push(DatabaseSession())


@socketio.on("disconnect")
def on_disconnect():
    """ Handle sockets being disconnected. """

    assert (
        current_user.value not in ACTIVE_PLAYERS
    ), "Players should be cleaned up prior to disconnecting"

    try:
        user_id = current_user.id
    except ProxyAccessError:
        LOGGER.debug("Disconnecting client that failed to log in.")
    else:
        if user_id in PLAYERS:
            player = PLAYERS[user_id]
            emit("player_logout", player.json, broadcast=True)
            player.store(player.uuid)
            LOGGER.debug(f"{current_user} disconnected")
        else:
            LOGGER.debug(f"{current_user}'s player already removed from world")
        current_user.pop()

    database_session.close()
    database_session.pop()


def monitor_players():
    """ Watch for players who haven't pinged the server in a while and log them out. """

    def check_players():
        for user in list(ACTIVE_PLAYERS):
            deadline = datetime.today() - timedelta(seconds=INACTIVE_TIMEOUT)
            inactive = user.last_seen < deadline
            LOGGER.debug(
                f"Checking {user} for inactivity: "
                f"{user.last_seen.strftime('%H:%M:%S')} "
                f"< {deadline.strftime('%H:%M:%S')} "
                f"== {inactive}"
            )
            if inactive:
                ACTIVE_PLAYERS.remove(user)

                LOGGER.info(f"Logging out {user} due to inactivity")

                socketio.emit("player_logout", user.id)

    with app.app_context():
        while True:
            check_players()
            eventlet.sleep(5)


eventlet.spawn(monitor_players)
