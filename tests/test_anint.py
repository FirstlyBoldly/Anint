# Built-ins
import pathlib

# Anint
from anint import translations

# Third-party
import pytest

locales: pathlib.Path = pathlib.Path(".") / "locales"


class TestTranslations:
    def test_return_value0(self):
        translations.load(str(locales))
        print(translations.data)
