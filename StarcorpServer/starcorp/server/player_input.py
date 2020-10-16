""" Module for all player input related events. """


from flask_socketio import emit
from global_context import PLAYERS, RESOURCE_NODES
from world.coordinates import Coordinate

from server import login_required, socketio

from objects import Player


@socketio.on("player_move")
@login_required
def move_player(user, message):

    player = Player.by_user(user)

    destination = Coordinate.load(message["destination"])
    print(f"Processing player movement request to {destination}")

    # TODO: Spend AP for movement

    try:
        player.move_to(destination)
    except ValueError:
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

    player = Player.by_user(user)

    target = Coordinate.load(message["target"])

    if target not in RESOURCE_NODES:
        emit(
            "gather_denied",
            {"message": f"Unable to gather at {target}: No resource node present"},
        )
    elif target != player.position:
        emit(
            "gather_denied", {"message": f"Unable to gather at {target}: Too far away"}
        )
    else:
        resource = RESOURCE_NODES[target]

        player.resources[resource] += 5
        player.store(player.uuid)

        emit("resource_gathered", player)