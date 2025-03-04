"""Constants of Anint."""

# Built-ins
from enum import StrEnum


class AnintDict(StrEnum):
    """Container enum for the project and its configuration."""

    TOOL = "tool"
    ANINT = "anint"
    LOCALES = "locales"
    LOCALE = "locale"
    FALLBACKS = "fallbacks"
    PATH = "path"
