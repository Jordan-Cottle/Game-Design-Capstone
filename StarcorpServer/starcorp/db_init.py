from models import Base
from database.static import push_config
from database.session import ENGINE

from data import Resource
from models import ResourceType
from database import DatabaseSession

from utils import get_logger

LOGGER = get_logger(__name__)


def main():
    """ Initialize database data. """
    LOGGER.info("Creating/validating models")
    Base.metadata.create_all(ENGINE)

    with DatabaseSession() as session:
        for resource_type in Resource:
            resource = ResourceType(name=resource_type)

            session.add(resource)

    push_config()


if __name__ == "__main__":
    main()