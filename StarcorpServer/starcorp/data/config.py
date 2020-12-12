""" Module for classes and logic related to accessing configuration data. """

import os

import yaml


class Config:
    """ Utility for accessing config data easily."""

    def __init__(self, file_name=None) -> None:
        if file_name is None:
            file_name = os.getenv("CONFIG")

        self.file_name = file_name

        with open(file_name, "r") as config_file:
            self.data = yaml.safe_load(config_file)

    def get(self, path):
        """Get a value from the config.

        path -- A "." seperated path to the value desired
        """

        steps = path.split(".")

        curr = self.data
        for step in steps:
            curr = curr[step]

        return curr

    def __str__(self) -> str:
        return f"Config file: {self.file_name}"


CONFIG = Config()
