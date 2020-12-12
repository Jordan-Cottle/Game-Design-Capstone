""" Package for providing access to data and processing utilities. """
# pylint: disable=wrong-import-position

import os

STORAGE_DIR = os.environ["DATA_STORE"]

from .config import CONFIG
from .constants import Resource
from .json_util import TYPE_META, Decoder, Encoder, Serializable, from_json, to_json
