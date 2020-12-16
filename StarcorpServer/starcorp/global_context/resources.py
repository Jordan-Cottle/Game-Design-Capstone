""" Module for providing global resource data. """

from data import Resource

from world.coordinates import Coordinate

# TODO: Implement ResourceNode to handle variability in the quality of nodes
# TODO: track resources on a world layer instead
RESOURCE_NODES = {
    Coordinate(0, 2, -2): Resource.WATER,
    Coordinate(1, 0, -1): Resource.WATER,
    Coordinate(-1, 0, 1): Resource.FOOD,
    Coordinate(-3, 0, 3): Resource.FUEL,
}
