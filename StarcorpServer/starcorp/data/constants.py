""" Module for enums and constants. """

from enum import Enum


class Resource(str, Enum):
    """Enumeration of all resource types in the game.

    These item types are the kinds of items players can gather or collect from the world
    and account for resources that cities require and loot from defeating mobs.
    """

    FOOD = "food"
    WATER = "water"
    FUEL = "fuel"
    ORE = "ore"
