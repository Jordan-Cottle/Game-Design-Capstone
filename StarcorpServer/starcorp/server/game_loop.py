""" Module for defining the server's internal game loop. """

import time
from models import Sector
from database import DatabaseSession

from data import CONFIG
from utils import get_logger

LOGGER = get_logger(__name__)

import eventlet

TICK_DURATION = CONFIG.get("game.tick_duration")


def main_loop():
    """ The server's internal game loop. """

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


def tick(session):
    """ Process a single game tick. """

    for sector in session.query(Sector).all():
        generate_resources(session, sector)


def generate_resources(session, sector):
    """ Generate resources for players to gather in a sector. """

    LOGGER.debug(f"Generating resources for {sector}")
