"""Anint: Ankha's Internationalization and Localization for Python."""

# Built-ins
import importlib.metadata

__version__: str = importlib.metadata.version("anint")

__all__: list[str] = [
    "t",
    "Translator",
    "TranslationError",
    "AnintConfigError",
    "MultipleSameLocaleError",
    "translations",
]

# Anint
from .setup import t
from .models import Translator
from .exceptions import TranslationError, AnintConfigError, MultipleSameLocaleError
from . import translations
