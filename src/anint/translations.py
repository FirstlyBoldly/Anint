"""Module for the translations."""

__all__: list[str] = ["load", "get"]

# Built-ins
from typing import Any
import json
import os

# Third-party
import yaml

# Anint
from .utils import parse_key
from .exceptions import TranslationError, MultipleSameLocaleError

translations: dict[str, Any] = {}


def load_yaml(filename: str) -> dict[str, Any]:
    with open(filename, "r") as file:
        return yaml.safe_load(file)


def load_json(filename: str) -> dict[str, Any]:
    with open(filename, "r") as file:
        return json.load(file)


def load(path_to_locale: str) -> None:
    """Load the translation from the given path_to_locale.

    :param str path_to_locale: Path to the translation file or directory containing the translation file.
    :return: None.
    :raise FileNotFoundError: If the requested file does not exist.
    """
    filepath: str = os.path.basename(path_to_locale)
    locale, extension = os.path.splitext(filepath)
    if locale not in translations:
        match extension:
            case ".yaml":
                translations[locale] = load_yaml(path_to_locale)
            case ".json":
                translations[locale] = load_json(path_to_locale)
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
        value: dict = translations[locale]
        for parsed_key in parsed_keys:
            value = value[parsed_key]

        if isinstance(value, str):
            return value
        else:
            raise TranslationError(key)
    except KeyError:
        raise TranslationError(key)
