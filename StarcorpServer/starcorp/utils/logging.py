""" Module for logging configuration. """

import os
import sys
import logging

from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from data import CONFIG

LOGGING_CONFIG = CONFIG.get("logging.application")

# create formatter
FORMATTER = logging.Formatter(
    CONFIG.get("logging.format"), datefmt=CONFIG.get("logging.date_format")
)

LOGGER_NAME = "starcorp"
# create logger
LOGGER = logging.getLogger(LOGGER_NAME)
LOGGER.setLevel(LOGGING_CONFIG["level"])
# create file handler and set level to debug
file_handler = RotatingFileHandler(**LOGGING_CONFIG["handler"])
file_handler.setLevel(LOGGING_CONFIG["level"])
file_handler.setFormatter(FORMATTER)
LOGGER.addHandler(file_handler)


if CONFIG.get("logging.console"):
    # create console handler and set level to debug
    console_handler = StreamHandler(stream=sys.stdout)
    console_handler.setLevel(LOGGING_CONFIG["level"])
    console_handler.setFormatter(FORMATTER)
    LOGGER.addHandler(console_handler)


def get_logger(name):
    """ Utility for getting a child of the configured logger. """
    return logging.getLogger(f"{LOGGER_NAME}.{name}")
