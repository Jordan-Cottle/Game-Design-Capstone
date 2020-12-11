""" Package for providing access to data and processing utilities. """
# pylint: disable=wrong-import-position

import os

STORAGE_DIR = os.environ["DATA_STORE"]


from .json_util import from_json, to_json, Decoder, Encoder, Serializable
