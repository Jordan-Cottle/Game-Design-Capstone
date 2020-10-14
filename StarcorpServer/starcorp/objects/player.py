from data.json_util import dumps, loads

from objects.gameobject import GameObject


class Player(GameObject):
    """ Represent a player. """

    def __init__(self):
        super().__init__()
        self.name = "Player"

    @property
    def json(self):
        return dumps(self.__dict__)

    @classmethod
    def load(cls, data):
        super().load(data)

        player = cls()

        for key, value in data.items:
            player.__dict__[key] = loads(value)

        return player

    def valid_position(self, position):
        return position in self.position.neighbors

    def __str__(self):
        return f"{self.name} @ {self.position}"

    def __repr__(self):
        return f"Player ({self.name}): {self.uuid}"
