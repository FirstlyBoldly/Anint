__all__: list[str] = ["data"]

# Built-ins
import configparser, tomllib, os
from configparser import ConfigParser
from typing import Any

# Anint
from .exceptions import AnintConfigError


def load_ini(filename: str) -> dict[str, Any]:
    config_data: ConfigParser = configparser.ConfigParser()
    config_data.read(filename)
    dict_data: dict[str, Any] = {}
    for section in config_data.sections():
        items: list[tuple[str, str]] = config_data.items(section)
        dict_data[section] = dict(items)

    return dict_data


def load_toml(filename: str) -> dict[str, Any]:
    with open(filename, "rb") as f:
        return tomllib.load(f)


def load_config(filename: str) -> dict[str, Any]:
    extension: str = os.path.splitext(filename)[1][1:]
    if extension == "ini" or extension == "cfg":
        return load_ini(filename)
    elif extension == "toml":
        return load_toml(filename)
    else:
        raise AnintConfigError()


def fetch_config_file() -> str:
    for filename in [
        "anint.ini",
        ".anint.ini",
        "pyproject.toml",
        "anint.cfg",
        "~/.anint.ini",
    ]:
        if os.path.exists(filename):
            return filename
    else:
        raise AnintConfigError()


data: dict[str, Any] = load_config(fetch_config_file())
