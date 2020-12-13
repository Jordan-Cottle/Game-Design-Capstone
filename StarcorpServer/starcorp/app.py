""" Main entrypoint for the Starcorp server. """
from utils import LOGGER

from server import socketio, app

from database.session import ENGINE
from models import Base

if __name__ == "__main__":
    LOGGER.info("Creating/validating models")
    Base.metadata.create_all(ENGINE)
    LOGGER.info("Starting server!")
    socketio.run(app, host="192.168.1.16", port="1234")
