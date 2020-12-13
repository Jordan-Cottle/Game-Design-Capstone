""" Module for game world relates models. """


from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship


from data import TileType

from models import Base


class Sector(Base):
    """ Model for associating data to a sector. """

    __tablename__ = "Sector"
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)

    ships = relationship("Ship", backref="sector", cascade="all, delete-orphan")
    cities = relationship("City", backref="sector", cascade="all, delete-orphan")
    tiles = relationship("Tile", backref="sector", cascade="all, delete-orphan")
    resource_nodes = relationship(
        "ResourceNode", backref="sector", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"Sector(id={self.id}, name={self.name})"


class Tile(Base):
    """ Model for tracking tile data. """

    __tablename__ = "Tile"
    id = Column(Integer, primary_key=True, autoincrement=True)

    position = Column(String, nullable=False, index=True)
    type = Column(Enum(TileType), nullable=False)

    sector_id = Column(Integer, ForeignKey("Sector.id"), nullable=False)

    sector = relationship("Sector")

    def __str__(self) -> str:
        return f"{self.type} tile @ {self.position} in {self.sector}"

    def __repr__(self) -> str:
        return (
            "Tile("
            f"id={self.id}, "
            f"position='{self.position}', "
            f"type={self.type}, "
            f"sector_id={self.sector_id})"
        )


class ResourceNode(Base):
    """ Model for tracking gatherable resource nodes. """

    __tablename__ = "ResourceNode"
    id = Column(Integer, primary_key=True)

    position = Column(String, nullable=False, index=True)

    resource_id = Column(Integer, ForeignKey("ResourceType.id"), nullable=False)
    sector_id = Column(Integer, ForeignKey("Sector.id"), nullable=False)

    sector = relationship("Sector")
    resource = relationship("Resource")

    def __str__(self) -> str:
        return f"{self.resource} node @ {self.position} in {self.sector}"

    def __repr__(self) -> str:
        return (
            "ResourceNode("
            f"id={self.id}, "
            f"position='{self.position}', "
            f"resource_id={self.resource_id}, "
            f"sector_id={self.sector_id})"
        )
