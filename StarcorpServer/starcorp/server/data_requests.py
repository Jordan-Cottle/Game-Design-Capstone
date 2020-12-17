""" Module for handling data requests from the client. """

from flask_socketio import emit

from database import get_cities, get_objects_in_sector
from global_context import CITIES, RESOURCE_NODES
from models import City, ResourceNode, Ship, Tile
from utils import get_logger
from world.coordinates import Coordinate
from server import current_user, database_session, login_required, socketio

LOGGER = get_logger(__name__)


@socketio.on("get_cities")
@login_required
def send_cities(message):  # pylint: disable=unused-argument
    """ Trigger a 'load_city' event for each city in the game. """
    LOGGER.debug(f"City list requested by {current_user}")
    for city in get_cities(database_session, current_user.ship.location.sector):
        resources = {}
        for resource_held in city.resources:
            resources[resource_held.resource.name] = resource_held.amount

        response = {
            "position": city.location.coordinate,
            "id": city.id,
            "name": city.name,
            "resources": resources,
            "population": city.population,
        }
        LOGGER.debug(f"Emitting {response} to {current_user}")
        emit("load_city", response)


@socketio.on("load_sector")
@login_required
def send_sector_data(message):  # pylint: disable=unused-argument
    """ Send sector data to user. """

    LOGGER.debug(f"Sector data requested by {current_user}")

    sector = current_user.ship.location.sector

    data = {
        "tiles": get_objects_in_sector(database_session, Tile, sector),
        "cities": get_objects_in_sector(database_session, City, sector),
        "ships": get_objects_in_sector(database_session, Ship, sector),
        "resource_nodes": get_objects_in_sector(database_session, ResourceNode, sector),
    }

    emit("sector_load", data)


@socketio.on("get_city_data")
@login_required
def get_city_data(message):
    """ Send the data for a city to the requesting player. """
    position = message["position"]

    city = CITIES.get(Coordinate.load(position))
    LOGGER.debug(f"{current_user} loading city {city}")
    if city:
        emit("update_city", city)


@socketio.on("get_resource_data")
@login_required
def get_resource_data(message):  # pylint: disable=unused-argument
    """ Send the position of all resource nodes to a player. """
    LOGGER.debug(f"Resource nodes requested by {current_user}")
    for position, resource in RESOURCE_NODES.items():
        emit("load_resource", {"position": position, "type": resource.name})
