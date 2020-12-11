""" Module for providing user classes and logic. """
import time
from hashlib import sha256

from data.json_util import Serializable


class User(Serializable):
    """ Class for handling user authentication. """

    def __init__(self, name):
        self.name = name
        self.last_seen = 0

    @property
    def id(self):
        """ Compute the id for a user. """
        return str(sha256(self.name.encode()).hexdigest())

    def ping(self):
        """ Update the timestamp for when the user was last seen. """
        self.last_seen = time.time()
        self.store(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def json(self):
        """ Return a json serializable representation of the user. """
        data = super().json

        data.update(self.__dict__)
        data["id"] = self.id

        return data

    @classmethod
    def load(cls, data):
        """ Load the user from a data dictionary. """
        user = cls(data["name"])

        user.__dict__.update(data)

        return user

    def __repr__(self):
        return f"{self.name}: {self.last_seen}"
