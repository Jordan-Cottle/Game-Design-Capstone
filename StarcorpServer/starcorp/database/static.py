""" Module for setting up and reading statically initialized values in the database. """

import yaml
from sqlalchemy.orm.exc import NoResultFound

from data import CONFIG, WORLD_CONFIG, ShipSystemAttributeType, TileType
from data.json_util import TYPE_META
from data.map_gen import load
from models import ResourceType, Sector, ShipChassis, ShipSystem, ShipSystemAttribute

from database import (
    DatabaseSession,
    create_city,
    get_by_name_or_id,
    get_chassis,
    get_cities,
    get_city,
    get_location,
    get_sector,
    get_ship_system,
    get_tile,
)
from models.world import Tile
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

    resource_data = []
    for resource_type in session.query(ResourceType).all():
        data = {"name": resource_type.name, "base_cost": resource_type.base_cost}
        resource_data.append(data)

    print(
        yaml.dump(
            {
                "Sector": sectors_data,
                "ShipChassis": ship_chassis_data,
                "ShipSystem": ship_system_data,
                "Resources": resource_data,
            },
            sort_keys=False,
        )
    )


def generate_resource(session, name, data):
    """ Add resource types to the database. """

    try:
        resource_type = get_by_name_or_id(session, ResourceType, name=name)
    except NoResultFound:
        resource_type = ResourceType(name=name, **data)
        session.add(resource_type)


def load_map(session, map_file, sector):
    """ Load a map of tiles into a sector. """

    map_data = load(map_file)

    rows = len(map_data)
    cols = len(map_data[0])

    r_start = -(rows // 2) + 1

    for x, row in enumerate(map_data, r_start):  # rows

        c_start = -(cols // 2) + 1
        for y, tile_type in enumerate(row, c_start):
            tile_type = TileType(tile_type)
            z = -(x + y)

            coordinate = Coordinate(x, y, z)

            tile = get_tile(session, sector, coordinate)
            if tile is None:
                tile = Tile(type=tile_type)
                tile.location = get_location(session, sector, coordinate)
                session.add(tile)
            elif tile.type != tile_type:
                print(f"Updating {tile} to {tile_type.name}")
                tile.type = tile_type


def generate_sectors(session, sectors_data):
    """ Get or create sectors using static config data. """
    print(sectors_data)
    for sector_name, sector_data in sectors_data.items():
        try:
            sector = get_sector(session, sector_name=sector_name)
        except NoResultFound:
            print(f"{sector_name} not in db, creating it")
            sector = Sector(name=sector_name)
            session.add(sector)

        cities_data = sector_data.pop("cities")
        for city_name, city_data in cities_data.items():
            try:
                get_city(session, city_name=city_name)
            except NoResultFound:
                print(f"{city_name} not found, creating it")
                coordinate = Coordinate.load(city_data["location"])
                location = get_location(session, sector, coordinate)
                create_city(session, city_name, location)

        load_map(session, f"data/maps/{sector.name}.map", sector)


def generate_chassis(session, chassis_data):
    """ Get or create chassis data from static config data. """

    print(chassis_data)

    for chassis_name, chassis_datum in chassis_data.items():
        try:
            chassis = get_chassis(session, name=chassis_name)
        except NoResultFound:

            chassis = ShipChassis(name=chassis_name, **chassis_datum)
            session.add(chassis)


def generate_ship_system(session, system_name, system_attributes_data):
    """ Generate a ship system with all of its attributes from config data. """

    print(system_attributes_data)
    try:
        ship_system = get_ship_system(session, name=system_name)
    except NoResultFound:
        print(f"Ship sub-system {system_name} not found, creating it.")

        ship_system = ShipSystem(name=system_name)
        session.add(ship_system)

        for attribute_type, value in system_attributes_data.items():
            print(f"Creating {attribute_type} = {value}")
            attribute = ShipSystemAttribute(
                type=ShipSystemAttributeType(attribute_type), value=value
            )
            ship_system.attributes.append(attribute)


def push_config():
    """ Push config data into the database. """

    session = DatabaseSession()

    for name, values in WORLD_CONFIG.get("Resources").items():
        generate_resource(session, name, values)

    generate_sectors(session, WORLD_CONFIG.get("Sector"))

    generate_chassis(session, WORLD_CONFIG.get("ShipChassis"))

    for name, system_data in WORLD_CONFIG.get("ShipSystem").items():
        generate_ship_system(session, name, system_data)

    session.commit()
    session.close()


if __name__ == "__main__":
    generate_empty_config()
