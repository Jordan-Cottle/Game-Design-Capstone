""" Module for defining the server's internal game loop. """

import random
import time
from collections import Counter

from data import CONFIG, WORLD_CONFIG
from database import DatabaseSession, create_resource_node, get_objects_in_sector
from models import Location, ResourceNode, ResourceType, Sector, Tile
from server import socketio
from utils import get_logger

LOGGER = get_logger(__name__)

import eventlet

TICK_DURATION = CONFIG.get("game.tick_duration")

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
            .join(Tile, Tile.type.in_(RESOURCE_TILES[name]))
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
        session.commit()
