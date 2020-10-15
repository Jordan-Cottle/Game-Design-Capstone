""" Utilities for serializing objects using the json module. """
import json
from abc import ABC, abstractmethod

from flask.json import JSONEncoder, JSONDecoder

TYPE_META = "__TYPE__"


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
            types[cls.__qualname__] = cls

        self.orig_obj_hook = kwargs.pop("object_hook", lambda data: data)
        super(CustomJSONDecoder, self).__init__(
            *args, object_hook=self.custom_obj_hook, **kwargs
        )

    def custom_obj_hook(data):
        object_type = data.get(TYPE_META)
        if object_type is None:
            return self.orig_obj_hook(data)

        return types[object_type].load(data)


def loads(data, **kwargs):
    return json.loads(data, object_hook=from_json, **kwargs)


def dumps(obj, **kwargs):
    return json.dumps(obj, default=to_json, **kwargs)
