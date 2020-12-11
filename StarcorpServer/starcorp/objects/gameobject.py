""" Base class for all objects that have a position tracked by the server. """
from abc import abstractmethod
from uuid import uuid4

from data.json_util import Serializable
from world.coordinates import Coordinate


class GameObject(Serializable):
    """ And object that has a position in the game world. """

    objects = {}

    def __init__(self):
        self.uuid = str(uuid4())
        self.position = Coordinate(0, 0, 0)

        GameObject.objects[self.uuid] = self

    @abstractmethod
    def valid_position(self, position):
        """ Determine if a position is a valid for this object. """

    @property
    def json(self):
        data = super().json

        data["uuid"] = self.uuid
        data["position"] = self.position.json

        return data

    @classmethod
    def load(cls, data):
        obj = cls()

        obj.uuid = data["uuid"]
        obj.position = Coordinate.load(data["position"])

        return obj

    def move_to(self, position):
        """ Move a game object to a new position. """
        if not self.valid_position(position):
            raise ValueError(f"{position} is invalid for {self}")

        self.position = position

    @staticmethod
    def get(uuid):
        """ Get the game object from storage based on its uuid. """
        return GameObject.objects.get(uuid)
