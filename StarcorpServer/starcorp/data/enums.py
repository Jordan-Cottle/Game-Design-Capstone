""" Module for enums and constants. """

from enum import Enum


class TileType(int, Enum):
    """ Enum for types of tiles in the world. """

    SPACE = 0
    GROUND = 1
    WATER = 2
    STAR = 3


class Resource(str, Enum):
    """Enumeration of all resource types in the game.

    These item types are the kinds of items players can gather or collect from the world
    and account for resources that cities require and loot from defeating mobs.
    """

    FOOD = "food"
    WATER = "water"
    FUEL = "fuel"
    ORE = "ore"


class ShipSystemAttributeType(str, Enum):
    """ Enumeration of all possible ship system attributes. """

    HARD_POINT_COST = "hard point cost"
    MODULE_COST = "module cost"
    COMPONENT_COST = "component cost"
    BASE_PRICE = "base price"

    MIN_POWER_DRAW = "minimum power draw"
    MAX_POWER_DRAW = "maximum power draw"

    POWER_EFFICIENCY = "power efficiency"
