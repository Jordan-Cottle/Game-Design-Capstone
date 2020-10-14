""" Module for all player input related events. """


from world.coordinates import Coordinate
from server import socketio

from flask_socketio import emit

from global_context import SESSIONS, PLAYER_LIST


@socketio.on("player_move")
def move_player(message):

    player = SESSIONS[message["session_id"]]

    destination = Coordinate.load(message["destination"])

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
            {"object_id": player.uuid, "destination": player.position},
            broadcast=True,
        )
