""" Package for defining all of the database models and their relationships. """
# pylint: disable=wrong-import-position

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .resources import ResourceType
from .user import User
