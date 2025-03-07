"""Initialize the translator method t from the given configuration file."""

# Built-ins
from typing import Callable

# Anint
from .constants import AnintDict
from .config import data
from .models import Translator
from . import translations

# Populate translations with the given absolute path.
translations.load(data[AnintDict.PATH])

# Initialize the method with the given values from the configuration file is any.
t: Callable[[str], str] = Translator(
    data[AnintDict.LOCALES],
    data[AnintDict.LOCALE],
    data[AnintDict.FALLBACKS],
).translate
