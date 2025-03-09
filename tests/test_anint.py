"""Tests for Anint."""

# Built-ins
import os
import pathlib

# Anint
from anint import translations
from anint import exceptions as err

# Third-party
import pytest

yaml_path: pathlib.Path = pathlib.Path(os.path.dirname(__file__)) / "locales" / "yaml"
json_path: pathlib.Path = pathlib.Path(os.path.dirname(__file__)) / "locales" / "json"
translations.load(str(yaml_path))


class TestTranslations:
    def test_return_value0(self):
        assert translations.get("en", "greetings.hello") == "Hello"

    def test_return_value1(self):
        assert translations.get("jp", "greetings.hello") == "こんにちは"

    def test_exception0(self):
        with pytest.raises(err.TranslationError):
            translations.get("en", "greetings.bye")
