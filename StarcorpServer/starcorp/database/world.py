""" Module for providing database utilities around getting and creating world data. """

from sqlalchemy.orm.exc import NoResultFound

from data import CONFIG
from models import City, CityResource, Location, ResourceNode, ResourceType, Sector
from utils import get_logger
from database import get_by_name_or_id

LOGGER = get_logger(__name__)


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
            .filter_by(sector_id=sector_id, position=coordinate.json)
            .one()
        )
    except NoResultFound:
        location = Location(sector_id=sector_id, position=coordinate.json)
        session.add(location)
        session.flush()

    return location


def get_tile(session, sector, coordinate):
    """ Get the tile from the database. """

    location = get_location(session, sector, coordinate)

    return location.tile


def create_resource_node(session, location, resource_type, amount):
    """ Create a new resource node in a sector. """

    node = ResourceNode(amount=amount)
    node.location = location
    node.resource = resource_type

    session.add(node)

    return node


def get_objects_in_sector(session, model, sector, count=False, **kwargs):
    """ Get objects of a type in a sector. """

    locations = session.query(Location).filter_by(sector_id=sector.id).subquery()

    query = session.query(model)

    query = query.filter_by(**kwargs)
    query = query.join(locations)

    if count:
        return query.count()
    else:
        return query.all()


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

    for resource_type in session.query(ResourceType).all():
        city_resource = CityResource(amount=0)
        city_resource.city = city
        city_resource.resource = resource_type

        session.add(city_resource)

    return city


def get_city_resource_slot(session, city, resource_type):
    """ Get the associated resource slot in a city. """
    return (
        session.query(CityResource)
        .filter_by(city_id=city.id, resource_id=resource_type.id)
        .one()
    )


def get_cost_of_resource(session, resource_type, amount, city):
    """ Sell a number of resources to a city. """

    city_resource = get_city_resource_slot(session, city, resource_type)

    return amount * city_resource.price