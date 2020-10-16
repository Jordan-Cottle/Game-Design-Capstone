""" Utilities for serializing objects using the json module. """
import os
from abc import ABC, abstractmethod

from data import STORAGE_DIR

from flask import json
from flask.json import JSONEncoder, JSONDecoder

TYPE_META = "__TYPE__"


def get_all_subclasses(cls):
    for sub_cls in cls.__subclasses__():
        yield sub_cls
        yield from get_all_subclasses(sub_cls)


def from_json(data, types={}):
    if not types:
        for cls in get_all_subclasses(Serializable):
            types[cls.__qualname__] = cls

    object_type = data.get(TYPE_META)
    if object_type is None:
        return data

    return types[object_type].load(data)


def to_json(obj):
    if not isinstance(obj, Serializable):
        raise TypeError(f"{obj} is not JSON serializable")

    return obj.json


class Encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Serializable):
            return obj.json

        return super().default(obj)


class Decoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        self.types = {}

        for cls in get_all_subclasses(Serializable):
            self.types[cls.__qualname__] = cls

        self.orig_obj_hook = kwargs.pop("object_hook", lambda data: data)
        super().__init__(*args, object_hook=self.custom_obj_hook, **kwargs)

    def custom_obj_hook(self, data):
        object_type = data.get(TYPE_META)
        if object_type is None:
            return self.orig_obj_hook(data)

        return self.types[object_type].load(data)


class Serializable(ABC):
    """ Mark a class as serializable by the json module. """

    @property
    @abstractmethod
    def json(self):
        """ Return a json serializable object representing this object. """

        return {TYPE_META: type(self).__qualname__}

    @classmethod
    @abstractmethod
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
        return self.__directory()

    @classmethod
    def file_name(cls, name):
        return os.path.join(cls.__directory(), str(name))

    def store(self, file_name):
        with open(self.file_name(file_name), "w") as data_file:
            json.dump(self, data_file)

    @classmethod
    def retrieve(cls, file_name):
        with open(cls.file_name(file_name), "r") as data_file:
            return json.load(data_file)