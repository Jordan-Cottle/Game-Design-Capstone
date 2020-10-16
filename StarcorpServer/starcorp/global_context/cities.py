from world.coordinates import Coordinate
from objects import City

CITIES = {}

c = City()
c.name = "Demoville"
c.population = 10

c.position = Coordinate(-4, 2, 2)

CITIES[c.position] = c