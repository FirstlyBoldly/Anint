"""Loaded data from the Anint configuration file if any."""

__all__: list[str] = ["data"]

# Built-ins
import configparser, tomllib, os
from configparser import ConfigParser
from typing import Any

# Anint
from .utils import get_file_extension, csv_to_list
from .exceptions import AnintConfigError
from .constants import AnintDict


def fetch_config_file() -> str:
    """Return the absolute path to the highest priority Anint configuration file.

    :return: Absolute path to the highest priority Anint configuration file.
    :raise AnintConfigError: If no matching config file is found.
    """
    for filepath in [
        f"{AnintDict.ANINT}.ini",
        f".{AnintDict.ANINT}.ini",
        "pyproject.toml",
        f"{AnintDict.ANINT}.cfg",
    ]:
        if os.path.exists(filepath):
            return os.path.abspath(filepath)
    else:
        raise AnintConfigError(
            "No recognized Anint configuration file found. Refer to README for writing the configuration file."
        )


def load_raw_ini(filepath: str) -> dict[str, Any]:
    """Return a dictionary of the Anint configuration from any .ini or .cfg file.

    :param str filepath: Path to the .ini or .cfg file.
    :return: Dictionary of the loaded values as is. *Beware that comma seperated values will not be converted to a list of elements.
    """
    config_data: ConfigParser = configparser.ConfigParser()
    config_data.read(filepath)
    return dict(config_data.items(AnintDict.ANINT))


def load_raw_toml(filepath: str) -> dict[str, Any]:
    """Return a dictionary of the Anint configuration from the pyproject.toml file.

    :param str filepath: Path to the .toml file.
    :return: Dictionary of the loaded values as is. *Beware that comma seperated values will not be converted to a list of elements.
    """
    with open(filepath, "rb") as f:
        return tomllib.load(f)[AnintDict.ANINT]


def load_config() -> dict[str, Any]:
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

    :return: Dictionary of the loaded Anint configuration. *Expects all keys to have a corresponding value, will assign empty values otherwise.
    :raise AnintConfigError: If the loaded file is not a .ini or .cfg or .toml file.
    """
    if filepath := fetch_config_file():
        filename: str = os.path.basename(filepath)
        extension: str = get_file_extension(filename)
        if extension == "ini" or extension == "cfg":
            config_data: dict[str, Any] = load_raw_ini(filepath)
        elif extension == "toml":
            config_data: dict[str, Any] = load_raw_toml(filepath)
        else:
            raise AnintConfigError(
                "The following {filename} is not a recognized configuration file format.".format(
                    filename=filename
                )
            )
    else:
        config_data: dict[str, Any] = {}

    # Normalize loaded config data.
    config_data[AnintDict.LOCALES] = csv_to_list(config_data.get(AnintDict.LOCALES, ""))
    config_data[AnintDict.LOCALE] = config_data.get(AnintDict.LOCALE, "")
    config_data[AnintDict.FALLBACKS] = csv_to_list(
        config_data.get(AnintDict.FALLBACKS, "")
    )
    config_data[AnintDict.PATH] = os.path.abspath(config_data.get(AnintDict.PATH, ""))

    return config_data


data: dict[str, Any] = load_config()
