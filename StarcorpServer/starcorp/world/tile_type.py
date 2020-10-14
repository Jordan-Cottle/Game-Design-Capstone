from enum import Enum


class TileType(int, Enum):
    SPACE = 0
    GROUND = 1
    WATER = 2
    STAR = 3
