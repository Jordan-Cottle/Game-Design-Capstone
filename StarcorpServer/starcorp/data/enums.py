""" Module for enums and constants. """

from enum import Enum


class TileType(str, Enum):
    """Enum for types of tiles in the world.

    These types represent types of planetary surfaces.
    """

    SPACE = " "
    LUSH = "L"
    ARID = "D"
    AQUATIC = "W"
    SOLAR = "*"

    def __str__(self) -> str:
        return str(self.value)


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

    HARD_POINT_COST = "hard_point_cost"
    MODULE_COST = "module_cost"
    COMPONENT_COST = "component_cost"
    BASE_COST = "base_cost"

    SPEED = "speed"
    POWER = "power"
    SIZE = "size"


class UnitType(str, Enum):
    """ Enumeration of all unit types in the game. """

    TRANSPORT = "transport"
    RAIDER = "raider"
    ALIEN = "alien"


class StructureType(str, Enum):
    """ Enumeration of all structure types in the game. """

    RESOURCE_YARD = "resource yard"
    FACTORY = "factory"
    TURRET = "turret"


class Action(str, Enum):
    """ Enumeration of available game actions. """

    ATTACK = "attack"
    GATHER = "gather"
    BUY = "buy"
    SELL = "sell"
    MOVE = "move"
    WAIT = "wait"
