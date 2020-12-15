""" Package for defining all of the database models and their relationships. """
# pylint: disable=wrong-import-position

from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.ext.declarative import declarative_base

from data import Serializable, TYPE_META


class SerializableTable(Serializable):
    """ Base table for all other tables. """

    @property
    def json(self):
        """ Return a json serializable representation of the table. """
        data = super().json

        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, ColumnProperty):
                data[prop.key] = getattr(self, prop.key)

        return data

    @classmethod
    def load(cls, data):
        """ Load a table instance from a dict. """

        super().load(data)

        return cls(**data)


Base = declarative_base(cls=SerializableTable)


from .city import City, CityResource
from .entities import Routine, Structure, Unit
from .resources import ResourceType
from .ships import (
    Ship,
    ShipChassis,
    ShipInstalledSystem,
    ShipInventory,
    ShipSystem,
    ShipSystemAttribute,
)
from .user import User
from .world import Location, ResourceNode, Sector, Tile
