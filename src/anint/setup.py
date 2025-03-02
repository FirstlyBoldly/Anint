# Built-ins
from typing import Callable

# Anint
from .constants import AnintDict
from .config import data
from .models import Translator
from . import translations

translations.load(data[AnintDict.PATH])

t: Callable[[str], str] = Translator(
    data[AnintDict.LOCALES],
    data[AnintDict.LOCALE],
    data[AnintDict.FALLBACKS],
    translations.data,
).translate
