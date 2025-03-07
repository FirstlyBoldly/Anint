"""Utility functions for Anint."""

# Built-ins
from re import split
from os.path import splitext
from typing import Union


def parse_key(key: str) -> list[str]:
    """Break up key into a list seperated by dots.

    :param str key: The key string.
    :return: A list of key values.
    """
    return split(r"\.", key)


def get_file_extension(filepath: str) -> str:
    """Extract the file extension from a given filepath.

    :param filepath: Specified file path.
    :return: Extension of the filepath.
    """
    return splitext(filepath)[1][1:]


def csv_to_list(list_string: Union[str, list]) -> list[str]:
    """Convert a comma separated string to a list of strings.

    :param list_string: A string of comma separated values.
    :return: A list of strings.
    """
    # If the input is a list, then return it as is.
    # Kinda hacky, but it works for data fetched from both toml and ini files.
    if isinstance(list_string, list):
        return list_string

    return [element.strip() for element in list_string.split(",")]
