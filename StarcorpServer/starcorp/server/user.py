import time
from uuid import uuid4

from data.json_util import Serializable


class User(Serializable):
    """ Class for handling user authentication. """

    def __init__(self, name):
        self.name = name
        self.user_id = str(uuid4())
        self.session_id = str(uuid4())
        self.last_seen = time.time()

    def ping(self):
        self.last_seen = time.time()

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    @property
    def json(self):
        data = super().json
        data["name"] = self.name
        data["user_id"] = self.user_id
        return data

    @classmethod
    def load(cls, data):
        user = User(data["name"])

        user.user_id = data["user_id"]

        return user
