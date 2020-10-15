import pytest
from data.json_util import dumps, loads
from world.layer import Layer
from world.tile_type import TileType


@pytest.fixture(name="tilemap")
def _tilemap(origin, a, b):
    layer = Layer()

    layer[origin] = TileType.GROUND
    layer[a] = TileType.SPACE
    layer[b] = TileType.WATER

    return layer


def test_serializable(tilemap, origin, a, b):
    data = dumps(tilemap)

    print(data)

    assert data == r'{"__TYPE__": "Layer", "0,0,0": 1, "1,2,-3": 0, "-4,1,3": 2}'
    reserialized = loads(data)

    assert tilemap[origin] == reserialized[origin]
    assert tilemap[a] == reserialized[a]
    assert tilemap[b] == reserialized[b]

    assert tilemap[a] == TileType.SPACE
    assert tilemap[b] == TileType.WATER
