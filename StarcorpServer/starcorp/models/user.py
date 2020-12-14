""" Module for defining user related models. """

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models import Base


class User(Base):
    """ Table for tracking the users of the game and their login info. """

    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)

    name = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    password = Column(String, nullable=False)

    ship = relationship("Ship", cascade="all, delete-orphan")

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"
