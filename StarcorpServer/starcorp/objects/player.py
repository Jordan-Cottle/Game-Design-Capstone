from objects.gameobject import GameObject

from global_context import PLAYERS

from objects import ALL_RESOURCES, User, Resource


class Player(GameObject):
    """ Represent a player. """

    def __init__(self):
        super().__init__()
        self.name = "Player"

        self.user = None
        self.resources = {}
        self.money = 0

    @classmethod
    def create(cls, name, user):
        player = cls()
        player.name = name
        player.user = user
        player.resources = {resource: 0 for resource in ALL_RESOURCES}
        player.money = 100

        player.store(player.uuid)

        PLAYERS[user.id] = player

        return player

    @staticmethod
    def by_user(user):
        return PLAYERS[user.id]

    def held(self, resource):
        return self.resources[resource]

    @property
    def json(self):
        data = super().json
        data["name"] = self.name

        data["user"] = self.user.json
        data["resources"] = {
            resource.name: value for resource, value in self.resources.items()
        }
        data["money"] = self.money

        return data

    @classmethod
    def load(cls, data):

        player = super().load(data)
        player.name = data["name"]

        player.user = User.load(data["user"])
        player.resources = {
            Resource.retrieve(resource): value
            for resource, value in data["resources"].items()
        }

        player.money = data["money"]

        return player

    def valid_position(self, position):
        return position in self.position.neighbors

    def __str__(self):
        return f"{self.name} @ {self.position}"

    def __repr__(self):
        return f"Player ({self.name}): {self.uuid}"
