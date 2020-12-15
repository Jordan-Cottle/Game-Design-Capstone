""" Module for game world relates models. """


from sqlalchemy import Column, Integer, String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship


from data import TileType

from models import Base


class Sector(Base):
    """ Model for associating data to a sector. """

    __tablename__ = "Sector"
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"Sector(id={self.id}, name={self.name})"


class Location(Base):
    """ Model for tracking specific locations in the world. """

    __tablename__ = "Location"
    __table_args__ = (
        UniqueConstraint("sector_id", "position", name="position_in_sector"),
    )

    id = Column(Integer, primary_key=True)

    position = Column(String, nullable=False, index=True)

    sector_id = Column(Integer, ForeignKey("Sector.id"), nullable=False, index=True)
    sector = relationship("Sector", uselist=False)

    tile = relationship("Tile", cascade="all, delete-orphan", uselist=False)
    city = relationship("City", cascade="all, delete-orphan", uselist=False)

    ships = relationship("Ship", cascade="all, delete-orphan")
    resource_nodes = relationship("ResourceNode", cascade="all, delete-orphan")

    def __str__(self) -> str:
        return f"{self.position}"

    def __repr__(self) -> str:
        return (
            "Location("
            f"id={self.id}, "
            f"position='{self.position}', "
            f"sector_id={self.sector_id})"
        )


class Tile(Base):
    """ Model for tracking tile data. """

    __tablename__ = "Tile"
    id = Column(Integer, primary_key=True, autoincrement=True)

    type = Column(Enum(TileType), nullable=False)

    location_id = Column(
        Integer, ForeignKey("Location.id"), unique=True, nullable=False, index=True
    )
    location = relationship("Location")

    def __str__(self) -> str:
        return f"{self.type} tile at {self.location}"

    def __repr__(self) -> str:
        return (
            "Tile("
            f"id={self.id}, "
            f"type={self.type}, "
            f"location_id={self.location_id})"
        )


class ResourceNode(Base):
    """ Model for tracking gatherable resource nodes. """

    __tablename__ = "ResourceNode"
    id = Column(Integer, primary_key=True)

    location_id = Column(Integer, ForeignKey("Location.id"), nullable=False, index=True)
    location = relationship("Location")

    resource_id = Column(Integer, ForeignKey("ResourceType.id"), nullable=False)
    resource = relationship("ResourceType")

    def __str__(self) -> str:
        return f"{self.resource} node at {self.location}"

    def __repr__(self) -> str:
        return (
            "ResourceNode("
            f"id={self.id}, "
            f"location_id={self.location_id}, "
            f"resource_id={self.resource_id})"
        )
