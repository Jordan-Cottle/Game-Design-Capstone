""" Module for all player input related events. """


from flask_socketio import emit

from database import add_resources, get_city, move_ship, sell_to_city
from server import current_user, database_session, login_required, socketio
from utils import get_logger
from world import Coordinate

LOGGER = get_logger(__name__)


def gather_resources(session, resource_node, gather_power):
    """ Attempt to gether resources from a node and return the amount found. """

    if resource_node.amount >= gather_power:
        amount = gather_power
    else:
        amount = resource_node.amount

    resource_node.amount -= amount
    LOGGER.debug(f"{amount} gathered from {resource_node}")

    if resource_node.amount <= 0:
        LOGGER.info(f"{resource_node} exhausted")
        emit(
            "resource_exhausted",
            {"position": resource_node.location.coordinate},
            broadcast=True,
        )
        session.delete(resource_node)

    return amount


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

    resource_node = ship.location.resource_node
    LOGGER.debug(f"Resource node == {resource_node}")

    if target != ship.location.coordinate:
        message = f"{ship} unable to gather at {target}: Too far away"
        LOGGER.warning(message)
        emit("gather_denied", {"message": message})
    elif ship.location.resource_node is None:
        message = f"{ship} unable to gather at {target}: No resource node present"
        LOGGER.warning(message)
        emit(
            "gather_denied",
            {"message": message},
        )
    elif ship.resources_held >= ship.carry_capacity:
        LOGGER.debug(f"{ship} unable to gather due to full storage")
        emit("gather_denied", {"message": "Ship storage full"})
    else:
        resource = resource_node.resource

        amount = gather_resources(database_session, resource_node, ship.gather_power)
        now_held = add_resources(database_session, resource, amount, ship)
        database_session.commit()

        emit(
            "resource_gathered", {"resource_type": resource.name, "now_held": now_held}
        )


@socketio.on("sell_resource")
@login_required
def sell_resource(message):
    """ Process resource sell request from a player. """

    ship = current_user.ship

    city = get_city(database_session, message["city_id"])

    LOGGER.debug(f"{ship} attempting to sell to {city}")

    if ship.location != city.location:
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
            profit, city_held = sell_to_city(
                database_session, resource_type, volume, city
            )
            current_user.money += profit

            database_session.commit()
            emit(
                "resources_sold",
                {
                    "new_balance": current_user.money,
                    "resource_type": resource_type.name,
                    "now_held": resource_slot.amount,
                    "city_id": city.id,
                    "city_held": city_held,
                },
            )
