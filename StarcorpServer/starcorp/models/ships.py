""" Module for modeling a Ship and all of it's components. """

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

from data import ShipSystemAttributeType
from models import Base


class ShipSystem(Base):
    """ Base definition for the different kinds of systems a ship can have. """

    __tablename__ = "ShipSystem"
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)

    attributes = relationship("ShipSystemAttribute", cascade="all, delete-orphan")

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"ShipSystem(id={self.id}, name={self.name})"

    def get_attribute(self, attribute):
        if attribute not in ShipSystemAttributeType:
            raise AttributeError(f"{self} does not have a {attribute} attribute")

        for system_attribute in self.attributes:
            if system_attribute.type == attribute:
                return system_attribute.value

        raise AttributeError(f"{self} does not have a {attribute} attribute")


class ShipSystemAttribute(Base):
    """ Table for tracking attributes of a ship system. """

    __tablename__ = "ShipSystemAttribute"
    id = Column(Integer, primary_key=True)

    __tableargs__ = (UniqueConstraint("type", "system_id"),)

    type = Column(Enum(ShipSystemAttributeType), nullable=False, index=True)
    value = Column(Float, nullable=False)

    system_id = Column(Integer, ForeignKey("ShipSystem.id"), nullable=False)
    system = relationship("ShipSystem")

    def __str__(self) -> str:
        return f"{self.system} {self.type} is {self.value}"

    def __repr__(self) -> str:
        return (
            f"ShipSystemAttribute("
            f"id={self.id}, "
            f"type='{self.type}', "
            f"value={self.value}, "
            f"system_id={self.system_id})"
        )


class ShipChassis(Base):
    """ Table for defining types of ship chassis available. """

    __tablename__ = "ShipChassis"
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    hull_points = Column(Integer, nullable=False)

    hard_points = Column(Integer, nullable=False)
    components = Column(Integer, nullable=False)
    modules = Column(Integer, nullable=False)

    base_cost = Column(Integer, nullable=False)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return (
            "ShipChassis("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"hull_points={self.hull_points}, "
            f"hard_points={self.hard_points}, "
            f"modules={self.modules}, "
            f"components={self.components}, "
            f"base_cost={self.base_cost})"
        )


class Ship(Base):
    """ Table for tracking all of the ships constructed in game. """

    __tablename__ = "Ship"
    id = Column(Integer, primary_key=True)

    active = Column(Boolean)

    location_id = Column(Integer, ForeignKey("Location.id"), nullable=False, index=True)
    location = relationship("Location")

    owner_id = Column(Integer, ForeignKey("User.id"), nullable=False, index=True)
    owner = relationship("User")

    chassis_id = Column(
        Integer, ForeignKey("ShipChassis.id"), nullable=False, index=True
    )
    chassis = relationship("ShipChassis")

    loadout = relationship("ShipInstalledSystem", cascade="all, delete-orphan")
    inventory = relationship("ShipInventory", cascade="all, delete-orphan")

    def __str__(self) -> str:
        return f"{self.owner.name}'s {self.chassis} ship at {self.location}"

    def __repr__(self) -> str:
        return (
            "Ship("
            f"id={self.id}, "
            f"active={self.active}, "
            f"location_id='{self.location_id}', "
            f"owner_id={self.owner_id}, "
            f"chassis_id={self.chassis_id})"
        )

    def __getattribute__(self, name):
        try:
            attr = ShipSystemAttributeType(name)
        except ValueError:
            return super().__getattribute__(name)
        else:
            return self.get_attribute(attr)

    def get_attribute(self, attribute):
        """ Get the value for an attribute. """

        if attribute not in ShipSystemAttributeType:
            raise AttributeError(f"{self} does not have a {attribute} attribute")

        total = 0
        for installed_system in self.loadout:
            try:
                total += installed_system.get_attribute(attribute)
            except AttributeError:
                continue

        return total


class ShipInstalledSystem(Base):
    """ Table for tracking the equipment on a ship. """

    __tablename__ = "ShipInstalledSystem"
    id = Column(Integer, primary_key=True)

    ship_id = Column(Integer, ForeignKey("Ship.id"), nullable=False, index=True)
    ship = relationship("Ship")

    system_id = Column(Integer, ForeignKey("ShipSystem.id"), nullable=False)
    system = relationship("ShipSystem")

    def __str__(self) -> str:
        return f"{self.system} installed on {self.ship}"

    def __repr__(self) -> str:
        return (
            "ShipInstalledSystem("
            f"id={self.id}, "
            f"ship_id={self.ship_id}, "
            f"system_id='{self.system_id}')"
        )

    def get_attribute(self, attribute):
        if attribute not in ShipSystemAttributeType:
            raise AttributeError(f"{self} does not have a {attribute} attribute")

        return self.system.get_attribute(attribute)


class ShipInventory(Base):
    """ Table for tracking the inventory contents of a ship. """

    __tablename__ = "ShipInventory"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, default=0, nullable=False)

    ship_id = Column(Integer, ForeignKey("Ship.id"), nullable=False, index=True)
    ship = relationship("Ship")

    resource_type_id = Column(Integer, ForeignKey("ResourceType.id"), nullable=False)
    resource_type = relationship("ResourceType")

    def __str__(self) -> str:
        return f"{self.amount} {self.resource_type} held by {self.ship}"

    def __repr__(self) -> str:
        return (
            "ShipInventory("
            f"id={self.id}, "
            f"amount={self.amount}, "
            f"ship_id={self.ship_id}, "
            f"resource_type_id='{self.resource_type_id}')"
        )
