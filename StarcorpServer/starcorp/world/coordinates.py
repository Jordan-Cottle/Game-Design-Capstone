""" The game world uses a hexagon tile grid indexed by cube cooridnates alone a plane. """

from data.json_util import Serializable


class Coordinate(Serializable):
    """A cubic coordinate vector.

    This class guarantees that all instances lie on the x+y+z = 0 plane.
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        assert x + y + z == 0, "All map coordinates must lie on a plane"

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __hash__(self):
        return (self.x << 16) | self.y

    def __str__(self):
        return f"<{self.x},{self.y},{self.z}>"

    @property
    def neighbors(self):
        """ Get all neighboring tiles. """
        return [self + offset for offset in DIRECTIONS]

    @property
    def json(self):
        return f"{self.x},{self.y},{self.z}"

    @classmethod
    def load(cls, data):
        return cls(*(int(datum) for datum in data.strip("\"'").split(",")))


DIRECTIONS = (
    Coordinate(1, -1, 0),
    Coordinate(1, 0, -1),
    Coordinate(0, 1, -1),
    Coordinate(-1, 1, 0),
    Coordinate(-1, 0, 1),
    Coordinate(0, -1, 1),
)
