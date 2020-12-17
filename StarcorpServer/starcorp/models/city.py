""" Module for city related models. """

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class City(Base):
    """ Model for tracking city data. """

    __tablename__ = "City"
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)
    population = Column(Integer, nullable=False)

    location_id = Column(
        Integer, ForeignKey("Location.id"), unique=True, nullable=False, index=True
    )
    location = relationship("Location")

    resources = relationship("CityResource", cascade="all, delete-orphan")

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return (
            "City("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"location={self.location}, "
            f"population={self.population}, "
            f"location_id={self.location_id})"
        )

    @property
    def json(self):
        """ Get json data to send to client. """

        return {
            "id": self.id,
            "position": self.location.coordinate.json,
            "name": self.name,
            "population": self.population,
            "resources": {
                resource_slot.resource.name: resource_slot.amount
                for resource_slot in self.resources
            },
        }


class CityResource(Base):
    """ Model for tracking which resources a city has. """

    __tablename__ = "CityResource"
    id = Column(Integer, primary_key=True)

    amount = Column(Integer, nullable=False)

    city_id = Column(Integer, ForeignKey("City.id"), nullable=False, index=True)
    city = relationship("City")

    resource_id = Column(
        Integer, ForeignKey("ResourceType.id"), nullable=False, index=True
    )
    resource = relationship("ResourceType", uselist=False)

    def __str__(self) -> str:
        return f"{self.city} has {self.amount} {self.resource}"

    def __repr__(self) -> str:
        return (
            "CityResource("
            f"id={self.id}, "
            f"amount={self.amount}, "
            f"city_id={self.city_id}, "
            f"resource_id={self.resource_id})"
        )

    @property
    def json(self):
        """ Send json data for client. """

        return {self.resource.name: self.amount}
