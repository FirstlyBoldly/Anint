__all__: list[str] = ["data"]

# Built-ins
import configparser, tomllib, os
from configparser import ConfigParser
from typing import Any

# Anint
from .utils import get_file_extension
from .exceptions import AnintConfigError

SECTION = "anint"


def load_ini(filename: str) -> dict[str, Any]:
    config_data: ConfigParser = configparser.ConfigParser()
    config_data.read(filename)
    return dict(config_data.items(SECTION))


def load_toml(filename: str) -> dict[str, Any]:
    with open(filename, "rb") as f:
        return tomllib.load(f)[SECTION]


def load_config(filename: str) -> dict[str, Any]:
    extension: str = get_file_extension(filename)
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
