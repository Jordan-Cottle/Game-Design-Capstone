import sys
import time
from hashlib import sha256
from uuid import uuid4

from data import STORAGE_DIR
from data.json_util import Serializable


class User(Serializable):
    """ Class for handling user authentication. """

    def __init__(self, name):
        self.name = name
        self.last_seen = time.time()

        self.store(self.id)

    @property
    def id(self):
        return str(sha256(self.name.encode()).hexdigest())

    def ping(self):
        self.last_seen = time.time()
        self.store(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def json(self):
        data = super().json
        data.update(self.__dict__)
        data["id"] = self.id
        return data

    @classmethod
    def load(cls, data):
        user = User(data["name"])

        user.__dict__.update(data)

        return user
