""" Module for providing database utilities around getting and creating world data. """

from sqlalchemy.orm.exc import NoResultFound

from database import get_by_name_or_id
from models import Sector, Location
def get_sector(session, sector_name=None, sector_id=None):
    """ Get a sector by it's name or id. """

    return get_by_name_or_id(session, Sector, model_id=sector_id, name=sector_name)


def get_location(session, sector, coordinate):
    """ Get or create a reference to the location for a coordinate in a sector. """

    try:
        sector_id = sector.id
    except AttributeError:
        assert isinstance(
            sector, int
        ), f"Expecting {sector} with no 'id' attribute to be an int"

        sector_id = sector

    try:
        location = (
            session.query(Location)
            .filter_by(id=sector_id, position=coordinate.json)
            .one()
        )
    except NoResultFound:
        location = Location(sector_id, coordinate)
        session.add(location)
        session.flush()

    return location
