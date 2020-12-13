""" Package for providing access to data and processing utilities. """
# pylint: disable=wrong-import-position

import os

STORAGE_DIR = os.environ["DATA_STORE"]

from .config import CONFIG
from .enums import Resource, ShipSystemAttributeType, TileType, UnitType, StructureType
from .json_util import TYPE_META, Decoder, Encoder, Serializable, from_json, to_json
