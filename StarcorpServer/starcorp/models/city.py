""" Module for city related models. """

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class City(Base):
    """ Model for tracking city data. """

    __tablename__ = "City"
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)
    position = Column(String, nullable=False)  # <x, y, z>
    population = Column(Integer, nullable=False)

    sector_id = Column(Integer, ForeignKey("Sector.id"), nullable=False, index=True)
    sector = relationship("Sector", backref="cities")
    resources = relationship(
        "CityResource", backref="city", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return (
            "City("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"position={self.position}, "
            f"population={self.population}, "
            f"sector_id={self.sector_id})"
        )


class CityResource(Base):
    """ Model for tracking which resources a city has. """

    __tablename__ = "CityResource"
    id = Column(Integer, primary_key=True)

    amount = Column(Integer, nullable=False)

    city_id = Column(Integer, ForeignKey("City.id"), nullable=False, index=True)
    resource_id = Column(
        Integer, ForeignKey("ResourceType.id"), nullable=False, index=True
    )

    city = relationship("City")
    resource = relationship("Resource")

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
