""" Module for resource related classes and logic. """

from data.json_util import Serializable


class Resource(Serializable):
    """ A collectable resource in the game. """

    def __init__(self, name, growth_weight, demand_ratio, base_price):
        self.name = name

        self.growth_weight = growth_weight
        self.demand_ratio = demand_ratio
        self.base_price = base_price

    def cost(self, demand):
        """ Calculate price for a single unit. """
        return self.base_price + (demand / 10000)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @property
    def json(self):
        """ Get json serializable form. """
        data = super().json

        data.update(self.__dict__)

        return data

    @classmethod
    def load(cls, data):
        """ reinstantiate Resource from data dictionary. """
        super().load(data)

        return cls(**data)

    def __str__(self):
        return self.name


FOOD = Resource.retrieve("food")
WATER = Resource.retrieve("water")
FUEL = Resource.retrieve("fuel")

ALL_RESOURCES = [FOOD, WATER, FUEL]
