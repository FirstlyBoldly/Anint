"""Loaded data from the Anint configuration file if any."""

__all__: list[str] = ["data", "instance_data"]

# Built-ins
import configparser
import tomllib
import os
from configparser import ConfigParser
from typing import Any, Optional

# Anint
from .utils import get_file_extension, csv_to_list
from .exceptions import AnintConfigError
from .constants import AnintDict

data: dict[str, Any] = {}
instance_data: dict[str, Any] = {}


def fetch_config_file() -> Optional[str]:
    """Return the absolute path to the highest priority Anint configuration file.

    :return: Absolute path to the highest priority Anint configuration file.
    :raise AnintConfigError: If no matching config file is found.
    """
    for filepath in [
        "{anint}.ini".format(anint=AnintDict.ANINT),
        ".{anint}.ini".format(anint=AnintDict.ANINT),
        "pyproject.toml",
        "{anint}.cfg".format(anint=AnintDict.ANINT),
    ]:
        if os.path.exists(filepath):
            return os.path.abspath(filepath)
    else:
        return None


def load_raw_ini(filepath: str) -> dict[str, Any]:
    """Return a dictionary of the Anint configuration from any .ini or .cfg file.

    :param str filepath: Path to the .ini or .cfg file.
    :return: Dictionary of the loaded values as is. *Beware that comma seperated values will not be converted to a list of elements.
    """
    config_data: ConfigParser = configparser.ConfigParser()
    config_data.read(filepath)
    try:
        return dict(config_data.items(AnintDict.ANINT))
    except configparser.NoSectionError:
        return {}


def load_raw_toml(filepath: str) -> dict[str, Any]:
    """Return a dictionary of the Anint configuration from the pyproject.toml file.

    :param str filepath: Path to the .toml file.
    :return: Dictionary of the loaded values as is. *Beware that comma seperated values will not be converted to a list of elements.
    """
    try:
        with open(filepath, "rb") as file:
            return tomllib.load(file)[AnintDict.TOOL][AnintDict.ANINT]
    except KeyError:
        return {}


def load_config(config_path: Optional[str] = None) -> None:
    """Return a dictionary of the Anint configuration.

    | An INI configuration file:
    | [anint]
    | locales = mn, en, jp
    | locale = jp
    | fallbacks = en
    | path = ./tests/locales
    |
    | Will be loaded as:
    | {
    | locales: ["mn", "en", "jp"],
    | locale: "jp",
    | fallbacks: ["en"],
    | path: "${PATH_TO_WORKING_DIRECTORY}/tests/locales"
    | }

    :param config_path: Optional path to the configuration file. Will have the highest precedence if given. None by default.
    :return: Dictionary of the loaded Anint configuration. *Expects all keys to have a corresponding value, will assign empty values otherwise.
    :raise AnintConfigError: If the loaded file is not a .ini or .cfg or .toml file.
    """
    global data, instance_data
    filepath: str = config_path or fetch_config_file()
    if filepath:
        filename: str = os.path.basename(filepath)
        extension: str = get_file_extension(filename)
        if extension == "ini" or extension == "cfg":
            data = load_raw_ini(filepath)
        elif extension == "toml":
            data = load_raw_toml(filepath)
        else:
            raise AnintConfigError(
                "The following {filename} is not a recognized configuration file format.".format(
                    filename=filename
                )
            )

    # Normalize loaded config data.
    data[AnintDict.LOCALES] = csv_to_list(data.get(AnintDict.LOCALES, []))
    data[AnintDict.LOCALE] = data.get(AnintDict.LOCALE, "")
    data[AnintDict.FALLBACKS] = csv_to_list(data.get(AnintDict.FALLBACKS, []))
    data[AnintDict.PATH] = os.path.abspath(data.get(AnintDict.PATH, ""))

    instance_data = {
        key: value
        for key, value in data.items()
        if key in [AnintDict.LOCALES, AnintDict.LOCALE, AnintDict.FALLBACKS]
    }


load_config()
