""" A Layer contains a map of data about every Tile in a sector. """
import json

from data.json_util import Serializable, from_json

from world.coordinates import Coordinate


class Layer(Serializable):
    """ Contains a map of locations related to data points. """

    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        if not isinstance(key, Coordinate):
            raise TypeError("Layers can only be indexed using cube coordinates")

        return self.data[key]

    def __setitem__(self, key, value):
        if not isinstance(key, Coordinate):
            raise TypeError("Layers can only be indexed using cube coordinates")

        self.data[key] = value

    @property
    def json(self):
        data = super().json
        data.update({coordinate.json: value for coordinate, value in self.data.items()})
        return data

    @classmethod
    def load(cls, data):
        super().load(data)

        layer = cls()
        for coordinate, value in data.items():
            coordinate = Coordinate.load(coordinate)

            if isinstance(value, dict):
                value = json.loads(value, object_hook=from_json)
            else:
                value = value

            layer[coordinate] = value

        return layer
