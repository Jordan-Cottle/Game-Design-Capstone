""" Module for providing global resource data. """

from objects import FOOD, WATER, FUEL

from world.coordinates import Coordinate


# TODO: Implement ResourceNode to handle variability in the quality of nodes
# TODO: track resources on a world layer instead
RESOURCE_NODES = {
    Coordinate(0, 2, -2): WATER,
    Coordinate(1, 0, -1): WATER,
    Coordinate(-1, 0, 1): FOOD,
    Coordinate(-3, 0, 3): FUEL,
}
