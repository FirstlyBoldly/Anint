"""Models for Anint."""

# Built-ins
from typing import Optional

# Anint
from .exceptions import TranslationError
from . import translations


class Translator:
    """Translator class."""

    def __init__(
        self,
        locales: list[str],
        locale: Optional[str] = None,
        fallbacks: Optional[list[str]] = None,
    ) -> None:
        """Initialize Translator class object.

        :param locales: List of available locales.
        :param locale: Specified locale.
        :param fallbacks: Fallback locales.
        :return: None.
        """
        self.locales: list[str] = locales
        self.locale: Optional[str] = locale
        self.fallbacks: Optional[list[str]] = fallbacks

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

    def translate(self, key: str, *args) -> str:
        """Returns the translation for the specified key.

        :param str key: A string sequence of dict keys connected by dots.
        :param args: Passed onto the translation to be formatted if there are any placeholders.
        :return: The translation for the currently specified language setting.
        """
        if not self.locale:
            raise ValueError(
                "Not specified locale exists. Set a locale to localize in."
            )

        try:
            value: str = translations.get(self.locale, key)
        except TranslationError:
            if not self.fallbacks:
                raise TranslationError(key)

            for fallback in self.fallbacks:
                try:
                    value = translations.get(fallback, key)
                    break
                except TranslationError:
                    pass
            else:
                raise TranslationError(key)

        return value.format(*args)
