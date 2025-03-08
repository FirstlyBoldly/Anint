"""Module for the translations."""

__all__: list[str] = ["load", "get"]

# Built-ins
from typing import Any
from pathlib import Path
import json
import os

# Third-party
import yaml

# Anint
from .utils import parse_key
from .exceptions import TranslationError, MultipleSameLocaleError

# Storage dictionary.
data: dict[str, Any] = {}


def load_yaml(filepath: str) -> dict[str, Any]:
    """Parse the given YAML file and return a dictionary.

    :param filepath: Absolute path to the YAML file.
    :return: Dictionary of the parsed YAML file.
    """
    with open(filepath, "r", encoding="utf8") as file:
        return yaml.safe_load(file)


def load_json(filepath: str) -> dict[str, Any]:
    """Parse the given JSON file and return a dictionary.

    :param filepath: Absolute path to the JSON file.
    :return: Dictionary of the parsed JSON file.
    """
    with open(filepath, "r", encoding="utf8") as file:
        return json.load(file)


def load(path_to_locale_directory: str) -> None:
    """Load the translation from the given path_to_locale_directory.

    :param str path_to_locale_directory: Path to the translation file or directory containing the translation file.
    :return: None.
    :raise FileNotFoundError: If the requested file does not exist.
    """
    for filepath in os.listdir(path_to_locale_directory):
        locale, extension = os.path.splitext(filepath)
        path_to_locale: Path = Path(path_to_locale_directory, filepath)
        extension = extension[1:]
        if locale not in data:
            match extension:
                case "yaml" | "yml":
                    data[locale] = load_yaml(str(path_to_locale))
                case "json":
                    data[locale] = load_json(str(path_to_locale))
        else:
            raise MultipleSameLocaleError(locale)


def get(locale: str, key: str) -> str:
    """Parse the locale data as is for the specified key.

    :param str locale: Specify which locale to get the translation from.
    :param str key: A string of dict keys combined by dots.
    :return: The translation for the current specified locale.
    :raise TranslationError: If the key raises a KeyError or if the referred value is not of type str.
    """
    try:
        parsed_keys: list[str] = parse_key(key)
        value: dict = data[locale]
        for parsed_key in parsed_keys:
            value = value[parsed_key]

        if isinstance(value, str):
            return value
        else:
            raise TranslationError(
                "{key} argument does not represent a localizable value".format(key=key)
            )
    except KeyError:
        raise TranslationError(key)
