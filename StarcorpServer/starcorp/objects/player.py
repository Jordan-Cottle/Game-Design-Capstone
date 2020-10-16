from objects.gameobject import GameObject


class Player(GameObject):
    """ Represent a player. """

    def __init__(self):
        super().__init__()
        self.name = "Player"

    @classmethod
    def create(cls, name):
        player = cls()
        player.name = name

        player.store(player.name)

        return player

    @property
    def json(self):
        data = super().json
        data["name"] = self.name

        return data

    @classmethod
    def load(cls, data):

        player = super().load(data)
        player.name = data["name"]

        return player

    def valid_position(self, position):
        return position in self.position.neighbors

    def __str__(self):
        return f"{self.name} @ {self.position}"

    def __repr__(self):
        return f"Player ({self.name}): {self.uuid}"
