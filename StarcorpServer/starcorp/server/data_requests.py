""" Module for handling data requests from the client. """

from global_context import CITIES, RESOURCE_NODES

from world.coordinates import Coordinate
from flask_socketio import emit
from server import socketio, login_required


@socketio.on("get_cities")
@login_required
def get_cities(user, message):
    print(f"City list requested by {user}")
    for city in CITIES.values():
        emit("load_city", city)


@socketio.on("get_city_data")
@login_required
def get_city_data(user, message):
    position = message["position"]

    city = CITIES.get(Coordinate.load(position))

    if city:
        emit("update_city", city)


@socketio.on("get_resource_data")
@login_required
def get_resource_data(user, message):
    print(f"Resource nodes requested by {user}")
    for position, resource in RESOURCE_NODES.items():
        emit("load_resource", {"position": position, "type": resource.name})
