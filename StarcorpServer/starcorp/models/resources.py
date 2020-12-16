""" Module for defining the resources model. """

from sqlalchemy import Column, Float, Integer, String

from models import Base


class ResourceType(Base):
    """ Table for tracking types of resources players can collect and trade. """

    __tablename__ = "ResourceType"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    base_cost = Column(Float, nullable=False)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"Resource(id={self.id}, name={self.name})"
