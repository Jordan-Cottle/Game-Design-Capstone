""" Utilities for serializing objects using the json module. """
import json
import os
from abc import ABC, abstractmethod

from flask.json import JSONDecoder, JSONEncoder

from data import STORAGE_DIR

TYPE_META = "__TYPE__"
TYPES = {}


def get_all_subclasses(cls):
    """ Recursively retrieve all subclasses of a class. """
    for sub_cls in cls.__subclasses__():
        yield sub_cls
        yield from get_all_subclasses(sub_cls)


def from_json(data):
    """ Reinstantiate a Serializable object from a json dictionary. """

    if not TYPES:  # Populate subclasses on first call
        for cls in get_all_subclasses(Serializable):
            TYPES[cls.__qualname__] = cls

    object_type = data.get(TYPE_META)
    if object_type is None:
        return data

    return TYPES[object_type].load(data)


def to_json(obj):
    """ Convert a Serializable object into json data. """

    if not isinstance(obj, Serializable):
        raise TypeError(f"{obj} is not JSON serializable")

    return obj.json


class Encoder(JSONEncoder):
    """ Custom encoder for Serializable objects. """

    def default(self, obj):  # pylint: disable=arguments-differ
        """ Handle detecting and converting Serializable objects. """

        if isinstance(obj, Serializable):
            return obj.json

        return super().default(obj)


class Decoder(JSONDecoder):
    """ Custom decoder for Serializable objects. """

    def __init__(self, *args, **kwargs):
        self.types = {}

        for cls in get_all_subclasses(Serializable):
            self.types[cls.__qualname__] = cls

        self.orig_obj_hook = kwargs.pop("object_hook", lambda data: data)
        super().__init__(*args, object_hook=self.custom_obj_hook, **kwargs)

    def custom_obj_hook(self, data):
        """ Detect and handle Serializable objects. """

        object_type = data.get(TYPE_META)
        if object_type is None:
            return self.orig_obj_hook(data)

        return self.types[object_type].load(data)


class Serializable:
    """ Mark a class as serializable by the json module. """

    @property
    def json(self):
        """ Return a json serializable object representing this object. """

        return {TYPE_META: type(self).__qualname__}

    @classmethod
    def load(cls, data):
        """ Reinstantiate an object from it's json data. """

        data.pop(TYPE_META)  # clean up for sub classes

    @classmethod
    def __directory(cls):
        directory = os.path.join(STORAGE_DIR, cls.__qualname__)

        os.makedirs(directory, exist_ok=True)
        return directory

    @property
    def directory(self):
        """ Get directory to store objects in. """

        return self.__directory()

    @classmethod
    def file_name(cls, name):
        """ Get filename for an object. """

        return os.path.join(cls.__directory(), str(name))

    def store(self, file_name):
        """ Serialize and store an object into a file. """

        with open(self.file_name(file_name), "w") as data_file:
            json.dump(self, data_file, cls=Encoder)

    @classmethod
    def retrieve(cls, file_name):
        """ Load an object from a file. """

        with open(cls.file_name(file_name), "r") as data_file:
            return json.load(data_file, cls=Decoder)
