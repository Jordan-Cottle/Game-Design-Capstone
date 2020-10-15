import pytest
from world.coordinates import Coordinate


@pytest.fixture(name="origin")
def _origin():
    return Coordinate(0, 0, 0)


@pytest.fixture(name="a")
def _a():
    return Coordinate(1, 2, -3)


@pytest.fixture(name="b")
def _b():
    return Coordinate(-4, 1, 3)
