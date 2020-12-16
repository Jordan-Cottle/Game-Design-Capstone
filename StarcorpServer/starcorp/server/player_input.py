""" Module for all player input related events. """


from flask_socketio import emit
from global_context import RESOURCE_NODES

from database import move_ship, add_resources
from objects import City, Resource
from server import current_user, database_session, login_required, socketio
from utils import get_logger
from world import Coordinate

LOGGER = get_logger(__name__)


@socketio.on("player_move")
@login_required
def move_player(message):
    """ Handle request for player movement. """

    ship = current_user.ship

    destination = Coordinate.load(message["destination"])
    LOGGER.debug(f"Processing player movement request to {destination}")

    # TODO: Spend AP for movement

    try:
        move_ship(database_session, ship, destination)
        database_session.commit()
    except ValueError:
        LOGGER.warning(f"{ship} movement to {destination} denied!")
        emit(
            "movement_denied",
            {"message": f"Unable to move to {destination} from {ship.location}"},
        )
    else:
        LOGGER.debug(f"{ship} moved to {ship.location}")
        emit(
            "object_moved",
            {"id": ship.id, "position": ship.location.coordinate},
            broadcast=True,
        )


@socketio.on("gather_resource")
@login_required
def gather_resource(message):
    """ Process gather resource request from player. """

    ship = current_user.ship

    target = Coordinate.load(message["target"])
    LOGGER.debug(f"{ship} attempting to gather at {target}")

    if target not in RESOURCE_NODES:
        message = f"{ship} unable to gather at {target}: No resource node present"
        LOGGER.warning(message)
        emit(
            "gather_denied",
            {"message": message},
        )
    elif target != ship.location.coordinate:
        message = f"{ship} unable to gather at {target}: Too far away"
        LOGGER.warning(message)
        emit("gather_denied", {"message": message})
    else:
        resource = RESOURCE_NODES[target]

        now_held = add_resources(database_session, resource, ship.gather_power, ship)
        database_session.commit()

        emit(
            "resource_gathered", {"resource_type": resource.value, "now_held": now_held}
        )


@socketio.on("sell_resource")
@login_required
def sell_resource(message):
    """ Process resource sell request from a player. """

    ship = current_user.ship

    city = City.get(message["city_id"])

    LOGGER.debug(f"{ship} attempting to sell to {city}")

    if ship.location.coordinate != city.position:
        message = f"{ship} unable to sell to {city}: Too far away"
        LOGGER.warning(message)
        emit(
            "gather_denied",
            {"message": message},
        )
    else:
        for resource_slot in ship.inventory:
            player_held = resource_slot.amount
            if 0 < player_held <= 5:
                volume = player_held
            elif player_held <= 0:
                continue
            else:
                volume = 5

            resource_type = resource_slot.resource_type

            LOGGER.info(f"{ship} selling {volume} {resource_type} units to {city}")

            resource_slot.amount -= volume
            profit = city.sell(Resource.retrieve(resource_type.name.value), volume)
            current_user.money += profit

            database_session.commit()
            emit(
                "resources_sold",
                {
                    "new_balance": current_user.money,
                    "resource_type": resource_type.name,
                    "now_held": resource_slot.amount,
                    "city": city,
                },
            )
