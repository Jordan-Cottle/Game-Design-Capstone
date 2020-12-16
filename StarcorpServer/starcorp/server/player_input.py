""" Module for all player input related events. """


from flask_socketio import emit
from global_context import RESOURCE_NODES

from database import move_ship, add_resources
from objects import ALL_RESOURCES, City, Player
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

        amount = ship.gather_power
        add_resources(database_session, resource, amount, ship)
        database_session.commit()

        emit("resource_gathered", {"resource_type": resource.value, "amount": amount})


@socketio.on("sell_resource")
@login_required
def sell_resource(message):
    """ Process resource sell request from a player. """

    player = Player.by_user(current_user)

    city = City.get(message["city_id"])

    LOGGER.debug(f"{player} attempting to sell to {city}")

    if player.position != city.position:
        message = f"{player} unable to sell to {city}: Too far away"
        LOGGER.warning(message)
        emit(
            "gather_denied",
            {"message": message},
        )
    else:
        for resource in ALL_RESOURCES:
            player_held = player.held(resource)
            if 0 < player_held <= 5:
                volume = player_held
            elif player_held <= 0:
                continue
            else:
                volume = 5

            LOGGER.info(f"{player} selling {volume} {resource} units to {city}")

            player.resources[resource] -= volume
            profit = city.sell(resource, volume)
            player.money += profit
            player.store(player.uuid)

        emit("resources_sold", {"player": player, "city": city})
