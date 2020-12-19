""" Module for ship related database utilities. """

from sqlalchemy.orm.exc import NoResultFound

from database import get_by_name_or_id, get_location
from models import (
    ResourceType,
    Ship,
    ShipChassis,
    ShipInstalledSystem,
    ShipInventory,
    ShipSystem,
)
from utils import get_logger


LOGGER = get_logger(__name__)


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


def add_resources(session, resource, amount, ship):
    """ Add resources to a ship's inventory. """

    if not isinstance(resource, ResourceType):
        resource = session.query(ResourceType).filter_by(name=resource).one()

    # check for existing slot to place resources in
    try:
        inventory_slot = (
            session.query(ShipInventory)
            .filter_by(ship_id=ship.id, resource_type_id=resource.id)
            .one()
        )
    except NoResultFound:
        LOGGER.debug(f"No inventory slot on {ship} found for {resource}, adding one")
        inventory_slot = ShipInventory()
        inventory_slot.resource_type = resource
        inventory_slot.ship = ship

        session.add(inventory_slot)
        session.commit()

    LOGGER.debug(f"Adding {amount} {resource} to {ship}: {inventory_slot}")
    inventory_slot.amount += amount

    return inventory_slot.amount


def get_upgrade(session, ship_system):
    """ Locate the next direct upgrade of a system. """

    name = ship_system.name

    model, make = name.split("Mk")
    make = int(make.strip())
    model = model.strip()

    models = session.query(ShipSystem).filter(ShipSystem.name.startswith(model)).all()

    for upgrade_model in models:
        if f"Mk {make+1}" in upgrade_model.name:
            LOGGER.debug(f"{ship_system} upgrades into {upgrade_model}")
            return upgrade_model

    LOGGER.debug(f"No upgrade found for {ship_system}")
    return None
