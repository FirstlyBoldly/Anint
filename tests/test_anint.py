"""Tests for Anint."""

# Built-ins
import os
import pathlib

# Anint
from anint import translations, config
from anint import exceptions as err
from anint.constants import AnintDict

# Third-party
import pytest

PATH = pathlib.Path(os.path.dirname(__file__))

LOCALE_PATH = PATH / "locales"
YAML_PATH = str(LOCALE_PATH / "yaml")
JSON_PATH = str(LOCALE_PATH / "json")
ERR_LOCALE_PATH = str(LOCALE_PATH / "err_locale_path")

CONFIG_PATH = PATH / ".config"
CONFIG0 = str(CONFIG_PATH / ".anint.ini")
CONFIG1 = str(CONFIG_PATH / "anint.ini")
CONFIG2 = str(CONFIG_PATH / "pyproject.toml")
CONFIG3 = str(CONFIG_PATH / "setup.cfg")
ERR_CONFIG0 = str(CONFIG_PATH / "anint.yaml")


# TODO
# Think of a better way of going about this...
@pytest.fixture
def flush():
    translations.flush()

class TestConfig:
    def test_return_value0(self):
        """If no configuration file is found, config.data and by extension config.instance_data
        should consist of empty values.
        """
        config.load_config()
        assert config.data == {
            AnintDict.LOCALES: [],
            AnintDict.LOCALE: "",
            AnintDict.FALLBACKS: [],
            AnintDict.PATH: os.path.abspath(""),
        }

    def test_return_value1(self):
        """Check if manually loading the configuration file will return the correct values."""
        for CONFIG in [CONFIG0, CONFIG1, CONFIG2, CONFIG3]:
            config.load_config(CONFIG)
            assert config.data[AnintDict.LOCALES] == ["mn", "en", "jp"]
            assert config.data[AnintDict.LOCALE] == "jp"
            assert config.data[AnintDict.FALLBACKS] == ["en"]
            assert config.data[AnintDict.PATH] == str(
                pathlib.Path().resolve() / "locales" / "yaml"
            )

    def test_exception0(self):
        with pytest.raises(err.AnintConfigError):
            config.load_config(ERR_CONFIG0)


class TestTranslations:
    @pytest.fixture
    def test_return_value0(self, flush):
        translations.load(YAML_PATH)
        assert translations.get("en", "greetings.hello") == "Hello"

    @pytest.fixture
    def test_return_value1(self, flush):
        translations.load(JSON_PATH)
        assert translations.get("jp", "greetings.hello") == "こんにちは"

    @pytest.fixture
    def test_exception0(self, flush):
        with pytest.raises(err.TranslationError):
            translations.load(YAML_PATH)
            translations.get("en", "greetings.bye")

    @pytest.fixture
    def test_exception1(self, flush):
        with pytest.raises(err.TranslationError):
            translations.load(ERR_LOCALE_PATH)
            translations.get("en", "greetings.hello")

    @pytest.fixture
    def test_exception2(self, flush):
        with pytest.raises(err.MultipleSameLocaleError):
            translations.load(ERR_LOCALE_PATH)
