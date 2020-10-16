""" Module for all player input related events. """


from flask_socketio import emit
from global_context import PLAYERS
from world.coordinates import Coordinate

from server import login_required, socketio


@socketio.on("player_move")
@login_required
def move_player(user, message):

    player = PLAYERS[user.id]

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
