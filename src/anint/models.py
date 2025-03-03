"""Models for Anint."""

# Built-ins
from typing import Optional

# Anint
from .exceptions import TranslationError
from .utils import parse_key


class Translator:
    """Translator class."""

    def __init__(
        self,
        locales: list[str],
        locale: Optional[str],
        fallback: Optional[str],
        translations: dict,
    ) -> None:
        """Initialize Translator class object.

        :param locales: List of available locales.
        :param locale: Specified locale.
        :param fallback: Fallback locale.
        :param translations: Translation dictionary.
        :return: None.
        """
        self.locales: list[str] = locales
        self.locale: str = locale
        self.fallback: Optional[str] = fallback
        self.translations: dict = translations

    def set_locale(self, locale: str) -> None:
        """Change the locale setting to the specified locale.

        :param str locale: The desired language code.
        :return: None.
        :raise ValueError: If locale not in the list of available locales.
        """
        if locale in self.locales:
            self.locale = locale
        else:
            raise ValueError(locale)

    def get(self, key: str, override_locale: Optional[str] = None) -> str:
        """Parse the locale data as is for the specified key.

        :param str key: A string of dict keys combined by dots.
        :param override_locale: Specify which locale to get the translation from. None by default.
        :return: The translation for the current specified language.
        :raise TranslationError: If the key raises a KeyError or if the referred value is not of type str.
        """
        try:
            parsed_keys: list[str] = parse_key(key)
            value: dict = self.translations[override_locale or self.locale]
            for parsed_key in parsed_keys:
                value = value[parsed_key]

            if isinstance(value, str):
                return value
            else:
                raise TranslationError(
                    "{key} argument does not represent a localizable value".format(
                        key=key
                    )
                )
        except KeyError:
            raise TranslationError(key)

    def translate(self, key: str, *args) -> str:
        """Returns the translation for the specified key.

        :param str key: A string sequence of dict keys connected by dots.
        :param args: Passed onto the translation to be formatted if there are any placeholders.
        :return: The translation for the currently specified language setting.
        """
        try:
            value: str = self.get(key)
        except TranslationError:
            if self.fallback:
                value: str = self.get(key, self.fallback)
            else:
                raise TranslationError(key)

        return value.format(*args)
