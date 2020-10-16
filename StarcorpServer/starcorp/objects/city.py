from flask import json

from objects import FOOD, FUEL, WATER, GameObject

from world.coordinates import Coordinate
from global_context import CITIES


class City(GameObject):
    """ Represent a city in the game. """

    def __init__(self):
        super().__init__()
        self.name = "City"
        self.population = 0
        self.resources = {
            FOOD: 5,
            WATER: 15,
            FUEL: 2,
        }

    def valid_position(self, position):
        """ Cities don't move. """
        return False

    @property
    def json(self):
        data = super().json
        data["name"] = self.name
        data["population"] = self.population
        data["resources"] = {
            resource.name: value for resource, value in self.resources.items()
        }

        return data

    @classmethod
    def load(cls, data):

        city = super().load(data)
        city.name = data["name"]
        city.population = data["population"]

        city.resources = {
            Resource.retrieve(name): value for name, value in data["resources"].items()
        }

        return player

    @property
    def growth(self):
        total_outstanding_demand = sum(
            (self.demand(resource) - self.volume(resource)) * resource.growth_weight
            for resource in self.resources
        )

        # TODO: figure out better equation for growth/demand
        growth = self.population - (total_outstanding_demand * 1.5)
        if growth > 0:
            # Cap to proportion of population
            growth = min(self.population * 0.5, growth)

        return int(growth)

    def volume(self, resource):
        return self.resources[resource]

    def demand(self, resource):
        demand = self.population * resource.demand_ratio
        return int(demand)

    def tick(self):
        for resource in self.resources:
            self.resources[resource] -= self.demand(resource)

            if self.volume(resource) < 0:
                self.resources[resource] = 0

        self.population += self.growth

    def sell(self, resource, volume):
        value = resource.cost(self.demand(resource)) * volume
        print(f"{volume} units of {resource} sold to {self}")
        self.resources[resource] += volume

        print(self.resources[resource], "units in stock at {self}")
        return value

    def __str__(self):
        return self.name


# TODO: move initialization of cities to a proper loading function
c = City()
c.name = "Demoville"
c.population = 10

c.position = Coordinate(-4, 2, 2)

CITIES[c.position] = c

c = City()
c.name = "Otherville"
c.population = 42

c.position = Coordinate(-2, 2, 0)

CITIES[c.position] = c