from data.json_util import loads, dumps
from world.coordinates import Coordinate

from itertools import permutations


def test_serializable(a):
    coordinate = Coordinate(1, 2, -3)

    data = dumps(coordinate)

    assert data == '"1,2,-3"', "Json was not the expected output"

    assert coordinate == Coordinate.load(
        data
    ), "Reserialization did not return an equal object"


def test_add(origin, a, b):
    assert origin + a == a
    assert origin + b == b

    assert a + b == Coordinate(-3, 3, 0)


def test_hash(origin, a, b):
    data = {origin: 0, a: 1, b: 2}

    assert data[origin] == 0
    assert data[a] == 1
    assert data[b] == 2


def test_neighbors(origin):
    neighbors = origin.neighbors

    assert origin not in neighbors, "A position cannot be its own neighbor"

    assert len(neighbors) == 6, "Each tile should have 6 neighbors"

    for permutation in permutations((-1, 0, 1), 3):
        expected = Coordinate(*permutation)

        assert expected in neighbors, "Neighbors is missing a value!"
