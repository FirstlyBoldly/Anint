__all__: list[str] = ["data"]

# Built-ins
import configparser, tomllib, os
from configparser import ConfigParser
from typing import Any

# Anint
from .constants import AnintDict
from .utils import get_file_extension, csv_to_list
from .exceptions import AnintConfigError


def load_raw_ini(filename: str) -> dict[str, Any]:
    config_data: ConfigParser = configparser.ConfigParser()
    config_data.read(filename)
    return dict(config_data.items(AnintDict.ANINT))


def load_raw_toml(filename: str) -> dict[str, Any]:
    with open(filename, "rb") as f:
        return tomllib.load(f)[AnintDict.ANINT]


def load_config(filename: str) -> dict[str, Any]:
    extension: str = get_file_extension(filename)
    if extension == "ini" or extension == "cfg":
        config_data: dict[str, Any] = load_raw_ini(filename)
    elif extension == "toml":
        config_data: dict[str, Any] = load_raw_toml(filename)
    else:
        raise AnintConfigError(filename)

    config_data[AnintDict.LOCALES] = csv_to_list(config_data.get(AnintDict.LOCALES, ""))
    config_data[AnintDict.FALLBACKS] = csv_to_list(
        config_data.get(AnintDict.FALLBACKS, "")
    )
    config_data[AnintDict.PATH] = os.path.abspath(config_data.get(AnintDict.PATH, ""))

    return config_data


def fetch_config_file() -> str:
    for filename in [
        f"./tests/.config/.{AnintDict.ANINT}.ini",
        f"{AnintDict.ANINT}.ini",
        f".{AnintDict.ANINT}.ini",
        "pyproject.toml",
        f"{AnintDict.ANINT}.cfg",
    ]:
        if os.path.exists(filename):
            return filename
    else:
        raise AnintConfigError()


data: dict[str, Any] = load_config(fetch_config_file())
