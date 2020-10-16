import pytest

from objects import Player, User

from world.coordinates import DIRECTIONS


@pytest.fixture(name="player")
def _player():
    return Player.create("TestPlayer", User("Test"))


def test_player_movement(player, a):
    with pytest.raises(ValueError):
        player.move_to(a)

    for direction in DIRECTIONS:
        new_pos = player.position + direction

        player.move_to(new_pos)

        assert player.position == new_pos


def test_serializable(player):
    data = player.json

    assert data["__TYPE__"] == "Player", "Json data should have the object's type"
    assert "uuid" in data, "Json data should have the object's uuid"
    assert data["position"] == "0,0,0", "Json data should have the object's position"

    assert data["name"] == "TestPlayer", "Json data should have the player's name"
    assert "user" in data, "Player should track which user it belongs to"
    assert data["resources"] == {"Food": 0, "Water": 0, "Fuel": 0}

    reinstantiated = Player.load(data)

    assert player.name == reinstantiated.name
    assert player.position == reinstantiated.position
    assert player.uuid == reinstantiated.uuid

    assert isinstance(
        reinstantiated, Player
    ), "Player type information was lost during serialization"
