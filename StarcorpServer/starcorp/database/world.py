from database import get_by_name_or_id
from models import Sector
def get_sector(session, sector_name=None, sector_id=None):
    """ Get a sector by it's name or id. """

    return get_by_name_or_id(session, Sector, model_id=sector_id, name=sector_name)
