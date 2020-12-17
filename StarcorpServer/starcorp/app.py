""" Main entrypoint for the Starcorp server. """
from utils import LOGGER

import eventlet

from server import socketio, app, main_loop


if __name__ == "__main__":
    LOGGER.info("Starting game loop")
    eventlet.spawn(main_loop)
    LOGGER.info("Starting server!")
    socketio.run(app, host="192.168.1.16", port="1234")
