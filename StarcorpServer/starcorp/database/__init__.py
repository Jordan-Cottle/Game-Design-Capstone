""" Module for providing access to the database. """

from .session import DatabaseSession


def get_by_name_or_id(session, model, *, model_id=None, name=None):
    """Get a model by it's id or by it's unique name.

    Preference is given to retriving by id.
    """

    if not (model_id or name):
        raise TypeError("model_id or name must be supplied!")

    filters = {}
    if model_id is not None:
        filters["id"] = model_id

    elif name is not None:
        filters["name"] = name

    sectors = session.query(model).filter_by(**filters).one()

    return sectors


from .user import create_user, login_user, get_user
from .world import (
    get_sector,
    get_location,
    get_city,
    get_cities,
    create_city,
    sell_to_city,
)
from .ship import get_chassis, get_ship_system, create_ship, move_ship, add_resources