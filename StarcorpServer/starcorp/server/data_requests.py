""" Module for handling data requests from the client. """

from global_context import CITIES

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