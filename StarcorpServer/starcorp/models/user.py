""" Module for defining user related models. """

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from utils import get_logger
from models import Base

LOGGER = get_logger(__name__)


class User(Base):
    """ Table for tracking the users of the game and their login info. """

    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)

    name = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    password = Column(String, nullable=False)

    last_seen = Column(DateTime, default=datetime.today, nullable=False)

    money = Column(Float, default=100, nullable=False)

    ship = relationship("Ship", cascade="all, delete-orphan", uselist=False)

    def ping(self):
        """ Update last seen time. """

        self.last_seen = datetime.today()
        LOGGER.debug(f"{self!r} ping at {self.last_seen.strftime('%H:%M:%S')}")

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"
