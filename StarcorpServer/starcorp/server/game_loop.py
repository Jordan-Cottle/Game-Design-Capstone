""" Module for defining the server's internal game loop. """

import random
import time
from collections import Counter
from functools import partial

from data import CONFIG, WORLD_CONFIG
from database import DatabaseSession, create_resource_node, get_objects_in_sector
from models import City, Location, ResourceNode, ResourceType, Sector, Tile
from server import socketio
from utils import get_logger


LOGGER = get_logger(__name__)

import eventlet

TICK_DURATION = CONFIG.get("game.tick_duration")
CONSUMPTION_RATIOS = CONFIG.get("game.cities.consumption")
CRITICAL_RESOURCES = CONFIG.get("game.cities.critical_resources")
GROWTH_RESOURCES = CONFIG.get("game.cities.critical_resources")

RESOURCE_TILES = {}
SECTOR_RESOURCE_TICKS = {}


def main_loop():
    """ The server's internal game loop. """

    with DatabaseSession() as session:
        setup(session)

    while True:
        start = time.time()
        with DatabaseSession() as session:
            tick(session)
        duration = time.time() - start

        if duration < TICK_DURATION:
            remaining = TICK_DURATION - duration
            LOGGER.info(f"Finished processing tick with {remaining}s left to spare")
            eventlet.sleep(remaining)
        else:
            LOGGER.warning(
                f"Server took {duration - TICK_DURATION}s too long to process a tick!"
            )


def setup(session):
    """ Perform one time setup operations. """

    resource_types = session.query(ResourceType).all()
    LOGGER.debug(f"Resource types available: {resource_types}")

    if not RESOURCE_TILES:
        resource_config = WORLD_CONFIG.get("Resources")
        for resource_type in resource_types:
            name = resource_type.name
            RESOURCE_TILES[name] = resource_config[name]["tile_types"]

    for sector in session.query(Sector).all():
        SECTOR_RESOURCE_TICKS[sector.name] = Counter()


def tick(session):
    """ Process a single game tick. """

    resource_types = session.query(ResourceType).all()

    for sector in session.query(Sector).all():
        generate_resources(session, sector, resource_types)

    for city in session.query(City).all():
        tick_city(city)
    session.commit()


def generate_resources(session, sector, resource_types):
    """ Generate resources for players to gather in a sector. """

    LOGGER.debug(f"Generating resources for {sector}")

    sector_resource_config = WORLD_CONFIG.get(f"Sector.{sector.name}.resources")

    for resource_type in resource_types:
        name = resource_type.name
        resource_config = sector_resource_config[name]

        resource_node_count = get_objects_in_sector(
            session, ResourceNode, sector, count=True, resource_id=resource_type.id
        )
        LOGGER.debug(
            f"{sector} has {resource_node_count} {resource_type} resource nodes"
        )

        if resource_node_count >= resource_config["max_nodes"]:
            LOGGER.debug(f"{sector} has enough {resource_type} nodes")
            continue

        resource_counter = SECTOR_RESOURCE_TICKS[sector.name]

        if resource_counter[name] < resource_config["rate"]:
            resource_counter[name] += 1
            LOGGER.debug(f"{name} resource counter at {resource_counter[name]}")
            continue

        LOGGER.debug(f"Attempting to spawn new {name}")
        resource_counter[name] = 0

        # TODO: Refactor into pre-generated resource spawn location table for direct access
        locations = (
            # Get all locations that are in this sector...
            session.query(Location)
            .filter_by(sector_id=sector.id)
            # and can spawn this kind of resource node...
            .join(Tile)
            .filter(Tile.type.in_(RESOURCE_TILES[name]))
            # and don't already have a node.
            .outerjoin(ResourceNode)
            .filter(ResourceNode.id == None)
            .all()
        )

        location = random.choice(locations)

        minimum, maximum = resource_config["amount_range"].split("-")
        minimum = int(minimum)
        maximum = int(maximum)

        amount = random.randint(minimum, maximum)

        node = create_resource_node(session, location, resource_type, amount)

        socketio.emit(
            "resource_generated",
            {"type": resource_type.name, "position": location.coordinate},
        )

        LOGGER.info(f"Resource node created: {node}")


def process_surplus(surplus, resource, city, city_slot):
    """ Process having a surplus of a resource. """

    if resource not in GROWTH_RESOURCES or surplus == 0:
        return

    growth = min(city.population // 100, surplus // CONSUMPTION_RATIOS[resource])
    LOGGER.info(f"{city} has enough surplus of {resource} to grow by {growth}")
    city_slot.amount -= growth * CONSUMPTION_RATIOS[resource]
    city.population += growth


def process_deficit(deficit, resource, city, city_slot):
    """ Process having a deficit of a resource. """

    city_slot.amount = 0

    if resource not in CRITICAL_RESOURCES:
        return

    casualties = deficit // CONSUMPTION_RATIOS[resource]
    LOGGER.debug(
        f"{city} starving from lack of {resource}: {casualties} population lost!"
    )
    city.population -= casualties


def tick_city(city):
    """ Process city resource consumption and growth. """

    city_volume = city.population // 100

    city_resources = {
        resource_slot.resource.name: resource_slot for resource_slot in city.resources
    }

    critical = False
    growth_triggers = []
    for resource, slot in city_resources.items():
        demand = CONSUMPTION_RATIOS[resource] * city_volume

        LOGGER.debug(f"{slot}")
        need = demand - slot.amount
        if need <= 0:
            LOGGER.debug(
                f"{city} has enough {resource} to consume {demand} with {-need} left over"
            )
            slot.amount -= demand
            growth_triggers.append(
                partial(process_surplus, -need, resource, city, slot)
            )
        else:
            LOGGER.debug(f"{city} does not have enough to consume {demand}")
            process_deficit(need, resource, city, slot)
            critical = True

    if not critical:
        for trigger in growth_triggers:
            trigger()

    LOGGER.info(f"{city} population {city.population} updated")
    socketio.emit("city_updated", city)
