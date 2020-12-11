""" Module for all player input related events. """


from flask_socketio import emit
from global_context import RESOURCE_NODES
from world.coordinates import Coordinate

from server import login_required, socketio

from objects import Player, City, ALL_RESOURCES
from utils import get_logger

LOGGER = get_logger(__name__)


@socketio.on("player_move")
@login_required
def move_player(user, message):
    """ Handle request for player movement. """

    player = Player.by_user(user)

    destination = Coordinate.load(message["destination"])
    LOGGER.debug(f"Processing player movement request to {destination}")

    # TODO: Spend AP for movement

    try:
        player.move_to(destination)
    except ValueError:
        LOGGER.warning(f"{player} movement to {destination} denied!")
        emit(
            "movement_denied",
            {"message": f"Unable to move to {destination} from {player.position}"},
        )
    else:
        emit(
            "object_moved",
            player,
            broadcast=True,
        )


@socketio.on("gather_resource")
@login_required
def gather_resource(user, message):
    """ Process gather resource request from player. """

    player = Player.by_user(user)

    target = Coordinate.load(message["target"])
    LOGGER.debug(f"{player} attempting to gather at {target}")

    if target not in RESOURCE_NODES:
        message = f"{player} unable to gather at {target}: No resource node present"
        LOGGER.warning(message)
        emit(
            "gather_denied",
            {"message": message},
        )
    elif target != player.position:
        message = f"{player} unable to gather at {target}: Too far away"
        LOGGER.warning(message)
        emit("gather_denied", {"message": message})
    else:
        resource = RESOURCE_NODES[target]

        player.resources[resource] += 5
        player.store(player.uuid)

        emit("resource_gathered", player)


@socketio.on("sell_resource")
@login_required
def sell_resource(user, message):
    """ Process resource sell request from a player. """

    player = Player.by_user(user)

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
