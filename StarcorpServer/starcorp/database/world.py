""" Module for providing database utilities around getting and creating world data. """

from sqlalchemy.orm.exc import NoResultFound

from database import get_by_name_or_id
from models import Sector, Location, City
from data import CONFIG


CITY_START_POP = CONFIG.get("game.cities.starting_population")


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


def get_objects_in_sector(session, model, sector):
    """ Get objects of a type in a sector. """

    locations = session.query(Location).filter_by(sector_id=sector.id).subquery()

    return session.query(model).join(locations).all()


def get_city(session, city_id=None, city_name=None):
    """ Get a city by it's name or id. """

    return get_by_name_or_id(session, City, model_id=city_id, name=city_name)


def get_cities(session, sector):
    """ Get cities based on the sector they are in. """

    return get_objects_in_sector(session, City, sector)


def create_city(session, name, location):
    """ Create a new city with the given name and location. """

    city = City(name=name, location_id=location.id, population=CITY_START_POP)

    session.add(city)

    return city
