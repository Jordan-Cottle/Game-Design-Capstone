import pytest

from objects.player import Player

from data.json_util import dumps, loads

from world.coordinates import DIRECTIONS


@pytest.fixture(name="player")
def _player():
    player = Player()
    player.name = "TestPlayer"

    return player


def test_player_movement(player, a):
    with pytest.raises(ValueError):
        player.move_to(a)

    for direction in DIRECTIONS:
        new_pos = player.position + direction

        player.move_to(new_pos)

        assert player.position == new_pos


def test_serializable(player):
    data = dumps(player)

    assert '"__TYPE__": "Player"' in data, "Json data should have the object's type"
    assert '"uuid": ' in data, "Json data should have the object's uuid"
    assert '"position": "0,0,0"' in data, "Json data should have the object's position"

    assert '"name": "TestPlayer"' in data, "Json data should have the player's name"

    reinstantiated = loads(data)

    assert player.name == reinstantiated.name
    assert player.position == reinstantiated.position
    assert player.uuid == reinstantiated.uuid

    assert isinstance(
        reinstantiated, Player
    ), "Player type information was lost during serialization"
