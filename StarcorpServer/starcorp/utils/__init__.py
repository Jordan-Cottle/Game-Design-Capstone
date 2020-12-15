""" Package for common utilities. """

from .logging import LOGGER, get_logger


def get_subclasses(cls):
    """ Get all subclasses of a class. """

    for sub_cls in cls.__subclasses__():
        yield from get_subclasses(sub_cls)
        yield sub_cls