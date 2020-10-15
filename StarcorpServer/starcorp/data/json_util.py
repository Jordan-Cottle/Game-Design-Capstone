""" Utilities for serializing objects using the json module. """
import json
from abc import ABC, abstractmethod

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

    print(data, type(data))

    return types[object_type].load(data)


def to_json(obj):
    if not isinstance(obj, Serializable):
        raise TypeError(f"{obj} is not JSON serializable")

    return obj.json


def loads(data, **kwargs):
    return json.loads(data, object_hook=from_json, **kwargs)


def dumps(obj, **kwargs):
    return json.dumps(obj, default=to_json, **kwargs)
