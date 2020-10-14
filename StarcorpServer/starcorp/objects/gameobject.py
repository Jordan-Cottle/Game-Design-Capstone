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

    def move_to(self, position):
        if not self.valid_position(position):
            raise ValueError(f"{position} is invalid for {self}")

        self.position = position

    @staticmethod
    def get(uuid):
        return GameObject.objects.get(uuid)
