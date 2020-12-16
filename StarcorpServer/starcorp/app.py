""" Main entrypoint for the Starcorp server. """
from utils import LOGGER

from server import socketio, app


if __name__ == "__main__":
    LOGGER.info("Starting server!")
    socketio.run(app, host="192.168.1.16", port="1234")
