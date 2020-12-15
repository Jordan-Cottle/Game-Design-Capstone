""" Module for ship related database utilities. """

from models import ShipChassis, ShipSystem
from database import get_by_name_or_id


def get_chassis(session, chassis_id=None, name=None):
    """ Get a ship chassis by it's id or name. """

    return get_by_name_or_id(session, ShipChassis, model_id=chassis_id, name=name)


def get_ship_system(session, system_id=None, name=None):
    """ Get a ship sub-system by its id or name. """

    return get_by_name_or_id(session, ShipSystem, model_id=system_id, name=name)