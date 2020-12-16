""" Module for ship related database utilities. """

from database import get_by_name_or_id, get_location
from models import Ship, ShipChassis, ShipInstalledSystem, ShipSystem


def get_chassis(session, chassis_id=None, name=None):
    """ Get a ship chassis by it's id or name. """

    return get_by_name_or_id(session, ShipChassis, model_id=chassis_id, name=name)


def get_ship_system(session, system_id=None, name=None):
    """ Get a ship sub-system by its id or name. """

    return get_by_name_or_id(session, ShipSystem, model_id=system_id, name=name)


def create_ship(session, user, location, chassis, loadout):

    ship = Ship(
        location_id=location.id, owner_id=user.id, chassis_id=chassis.id, active=True
    )

    session.add(ship)

    for item in loadout:
        system = ShipInstalledSystem(system_id=item.id)
        ship.loadout.append(system)

    session.flush()

    return ship


def move_ship(session, ship, coordinate):
    """ Attempt to move this ship to a new location. """

    if coordinate not in ship.location.coordinate.neighbors:
        raise ValueError(f"{ship} too far away from {coordinate}")

    ship.location = get_location(session, ship.location.sector, coordinate)
