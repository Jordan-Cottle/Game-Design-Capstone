import sys

from hashlib import sha256
import time
from uuid import uuid4

from flask_login import UserMixin

from data import STORAGE_DIR
from data.json_util import Serializable


class User(Serializable, UserMixin):
    """ Class for handling user authentication. """

    def __init__(self, name):
        self.name = name
        self.last_seen = time.time()

        self.store(self.user_id)

    @property
    def user_id(self):
        return str(sha256(self.name.encode()).hexdigest())

    def ping(self):
        self.last_seen = time.time()

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    def get_id(self):
        return self.user_id

    @property
    def json(self):
        data = super().json
        data.update(self.__dict__)
        data["user_id"] = self.user_id
        return data

    @classmethod
    def load(cls, data):
        user = User(data["name"])

        user.__dict__.update(data)

        return user
