""" Module for holding the tile type enumeration. """
from enum import Enum


class TileType(int, Enum):
    """ Enum for types of tiles in the world. """

    SPACE = 0
    GROUND = 1
    WATER = 2
    STAR = 3
