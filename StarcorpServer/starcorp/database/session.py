""" Class for setting up and managing database sessions. """

from sqlalchemy import engine_from_config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from data import CONFIG
from utils import get_logger

LOGGER = get_logger(__name__)


class Database:
    """ Class for managing a database engine. """

    def __init__(self, url=None) -> None:
        self.url = url

        self._engine = None

    def create_engine(self):
        """ Create a new engine. """

        config = CONFIG.get("database.engine")

        # Override url is set by constructor
        if self.url is not None:
            config["url"] = self.url

        return engine_from_config(config, prefix="")

    @property
    def engine(self):
        """ Lazy load an engine object. """

        if self._engine is None:
            self._engine = self.create_engine()

        return self._engine


ENGINE = Database().engine


class DatabaseSession:
    """ Class for managing a session lifecycle. """

    def __init__(self, bind=ENGINE) -> None:
        self.bind = bind

        self._session = None

    @property
    def session(self):
        """ Lazy load session when it is needed. """

        if self._session is None:
            self._session = Session(bind=self.bind)

        return self._session

    def __getattr__(self, name):
        return getattr(self.session, name)

    def __enter__(self):
        return self

    def __exit__(self, *args):  # pylint: disable=unused-argument
        if self._session is None:
            return

        try:
            self.session.commit()
        except SQLAlchemyError:
            LOGGER.exception("Database operation failed to commit, rolling back")
            self.session.rollback()
        else:
            self.session.close()
