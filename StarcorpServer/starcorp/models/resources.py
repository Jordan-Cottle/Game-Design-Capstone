""" Module for defining the resources model. """

from sqlalchemy import Column, Integer, Enum

from models import Base

from data import Resource


class ResourceType(Base):
    """ Table for tracking types of resources players can collect and trade. """

    __tablename__ = "ResourceType"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(Resource), unique=True, nullable=False, index=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"Resource(id={self.id}, name={self.name})"
