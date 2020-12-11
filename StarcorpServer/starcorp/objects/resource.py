from data.json_util import Serializable


class Resource(Serializable):
    """ A collectable resource in the game. """

    def __init__(self, name, growth_weight, demand_ratio, base_price):
        self.name = name

        self.growth_weight = growth_weight
        self.demand_ratio = demand_ratio
        self.base_price = base_price

    def cost(self, demand):
        return self.base_price + (demand / 10000)

    def __eq__(self, other):
        self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @property
    def json(self):
        data = super().json

        data.update(self.__dict__)

        return data

    @classmethod
    def load(cls, data):
        super().load(data)

        return cls(**data)

    def __str__(self):
        return self.name


FOOD = Resource.retrieve("Food")
WATER = Resource.retrieve("Water")
FUEL = Resource.retrieve("Fuel")

ALL_RESOURCES = [FOOD, WATER, FUEL]
