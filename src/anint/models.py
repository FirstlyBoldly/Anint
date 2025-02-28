"""Models for Anint."""

# Anint
from .exceptions import TranslationError
from .utils import _parse_key


class Translator:
    """Translator class."""

    def __init__(
        self, locales: list[str], locale: str, fallback: str, translations: dict
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
        self.fallback: str = fallback
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

    def get(self, key: str) -> str:
        """Parse the locale data as is for the specified key.

        :param str key: A string of dict keys combined by dots.
        :return: The translation for the current specified language.
        :raise TranslationError: If the key raises a KeyError or if the referred value is not of type str.
        """
        try:
            parsed_keys: list[str] = _parse_key(key)
            value: dict = self.translations[self.locale]
            for parsed_key in parsed_keys:
                value = value[parsed_key]

            if isinstance(value, str):
                return value
            else:
                raise TranslationError(key)
        except KeyError:
            raise TranslationError(key)

    def translate(self, key: str, *args) -> str:
        """Returns the translation for the specified key.

        :param str key: A string sequence of dict keys connected by dots.
        :param args: Passed onto the translation to be formatted if there are any placeholders.
        :return: The translation for the currently specified language setting.
        """
        translation: str = self.get(key)
        return translation.format(*args)
