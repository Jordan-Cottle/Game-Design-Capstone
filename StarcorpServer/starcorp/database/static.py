""" Module for setting up and reading statically initialized values in the database. """

import yaml
from sqlalchemy.orm.exc import NoResultFound

from data import CONFIG, ShipSystemAttributeType
from data.json_util import TYPE_META
from models import Sector, ShipChassis, ShipSystem, ShipSystemAttribute
from database import (
    DatabaseSession,
    create_city,
    get_chassis,
    get_city,
    get_location,
    get_sector,
    get_ship_system,
    get_cities,
)
from world.coordinates import Coordinate


def generate_empty_config():
    """ Generates an config file for adding values into by hand. """

    sectors = [{"name": '""', "cities": []}]
    ship_chassis = [
        {
            "name": '""',
            "base_cost": 0,
            "hull_points": 0,
            "hard_points": 1,
            "components": 1,
            "modules": 1,
        }
    ]
    ship_systems = [{"name": '""', "attributes": {"base_cost": 0}}]

    print(
        yaml.dump(
            {"Sector": sectors, "ShipChassis": ship_chassis, "ShipSystem": ship_systems}
        )
    )


def generate_config(empty=False):
    """ Generate a config file for adding static values by hand. """

    if empty:
        return generate_empty_config()

    session = DatabaseSession()

    sectors = session.query(Sector).all()

    print(sectors)
    sectors_data = []

    for sector in sectors:
        city_data = []
        sector_data = {"name": sector.name, "cities": city_data}

        cities = get_cities(session, sector)
        print(cities)
        for city in cities:
            city_data.append({"name": city.name, "location": city.location.position})

        sectors_data.append(sector_data)

    ship_chassis_data = []
    for chassis in session.query(ShipChassis).all():
        data = chassis.json
        data.pop(TYPE_META)
        data.pop("id")
        ship_chassis_data.append(data)

    print(ship_chassis_data)

    ship_system_data = []
    ship_systems = session.query(ShipSystem).all()
    for ship_system in ship_systems:
        attributes = {}
        data = {"name": ship_system.name, "attributes": attributes}
        for attribute in ship_system.attributes:
            attributes[attribute.type.value] = attribute.value

        ship_system_data.append(data)

    print(
        yaml.dump(
            {
                "Sector": sectors_data,
                "ShipChassis": ship_chassis_data,
                "ShipSystem": ship_system_data,
            },
            sort_keys=False,
        )
    )


def generate_sectors(session, sectors_data):
    """ Get or create sectors using static config data. """
    print(sectors_data)
    for sector_data in sectors_data:
        sector_name = sector_data["name"]

        try:
            sector = get_sector(session, sector_name=sector_name)
        except NoResultFound:
            print(f"{sector_name} not in db, creating it")
            sector = Sector(name=sector_name)
            session.add(sector)

        cities_data = sector_data.pop("cities")
        for city_data in cities_data:
            city_name = city_data["name"]

            try:
                get_city(session, city_name=city_name)
            except NoResultFound:
                print(f"{city_name} not found, creating it")
                coordinate = Coordinate.load(city_data["location"])
                location = get_location(session, sector, coordinate)
                create_city(session, city_name, location)


def generate_chassis(session, chassis_data):
    """ Get or create chassis data from static config data. """

    print(chassis_data)

    for chassis_datum in chassis_data:
        chassis_name = chassis_datum["name"]
        try:
            chassis = get_chassis(session, name=chassis_name)
        except NoResultFound:

            chassis = ShipChassis(**chassis_datum)
            session.add(chassis)


def generate_ship_system(session, system_data):
    """ Generate a ship system with all of its attributes from config data. """

    print(system_data)
    system_name = system_data["name"]
    try:
        ship_system = get_ship_system(session, name=system_name)
    except NoResultFound:
        print(f"Ship sub-system {system_name} not found, creating it.")

        system_attributes_data = system_data.pop("attributes")
        ship_system = ShipSystem(**system_data)
        session.add(ship_system)

        for attribute_type, value in system_attributes_data.items():
            print(f"Creating {attribute_type} = {value}")
            attribute = ShipSystemAttribute(
                type=ShipSystemAttributeType(attribute_type), value=value
            )
            ship_system.attributes.append(attribute)


def push_config():
    """ Push config data into the database. """

    with open(CONFIG.get("game.static_data")) as data_file:
        config = yaml.safe_load(data_file.read())

    session = DatabaseSession()

    generate_sectors(session, config["Sector"])

    generate_chassis(session, config["ShipChassis"])

    for system_data in config["ShipSystem"]:
        generate_ship_system(session, system_data)

    session.commit()
    session.close()


if __name__ == "__main__":
    generate_empty_config()
