""" Module for all player input related events. """


from data.json_util import dumps
from flask_socketio import emit
from global_context import PLAYER_LIST, SESSIONS
from world.coordinates import Coordinate

from server import socketio


@socketio.on("player_move")
def move_player(message):

    user = SESSIONS[message["session_id"]]
    player = PLAYER_LIST[user.name]

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
            {"uuid": player.uuid, "destination": dumps(player.position)},
            broadcast=True,
        )
