"""Models for Anint."""

# Anint
from .exceptions import TranslationError
from .utils import parse_key


class Translator:
    """Translator class."""

    def __init__(
        self, locales: list[str], locale: str, fallback: str, translations: dict
    ) -> None:
        self.locales: list[str] = locales
        self.locale: str = locale
        self.fallback: str = fallback
        self.translations: dict = translations

    def set_locale(self, locale: str) -> None:
        """Change the locale setting to a different language.

        :param str locale: The desired language code.
        :return: None.
        :raise ValueError: If locale not in locales.
        """
        if locale in self.locales:
            self.locale = locale
        else:
            raise ValueError(locale)

    def get(self, key: str) -> str:
        """Parse the locale data to get the translation.

        :param str key: A string of dict keys combined by dots.
        :return: The translation for the current specified language.
        :raise TranslationError: If the key raises a KeyError or if the referred value is not of type str.
        """
        try:
            parsed_keys: list[str] = parse_key(key)
            value: dict = self.translations[self.locale]
            for parsed_key in parsed_keys:
                value = value[parsed_key]

            if isinstance(value, str):
                return value
            else:
                raise TranslationError(key)
        except KeyError:
            raise TranslationError(key)

    def before_after(self, before: str, after: str) -> tuple[str, str]:
        """Returns a tuple of strings as (before, after) of the key translation."""
        before_translation: str = self.get(before) if before else ""
        after_translation: str = self.get(after) if after else ""
        return before_translation, after_translation

    def give_attention(self, attention: bool) -> str:
        """Returns an attention translation if attention is True, otherwise empty string."""
        return self.get("symbol.attention") if attention else ""

    def encapsulate(self, encapsulate: bool) -> tuple[str, str]:
        """Returns a tuple of encapsulations as (before, after) if encapsulate is True, otherwise tuple of empty strings."""
        encapsulate_before: str = ""
        encapsulate_after: str = ""
        if encapsulate:
            if self.locale == "ja":
                encapsulate_before = self.get("symbol.left_black_lenticular_bracket")
                encapsulate_after = self.get("symbol.right_black_lenticular_bracket")
            else:
                encapsulate_before = self.get("symbol.left_square_bracket")
                encapsulate_after = self.get("symbol.right_square_bracket")

        return encapsulate_before, encapsulate_after

    def translate(self, key: str, *args, **kwargs) -> str:
        """Returns the translation for the specified key.

        :param str key: A string sequence of dict keys connected by dots.
        :arg args: Passed onto the translation to be formatted if there are any placeholders.
        :keyword before: Optional key to be included to the left of the key translation.
        :keyword after: Optional key to be included to the right of the key translation.
        :keyword encapsulate: Whether to highlight translation.
        :keyword attention: Whether to give attention to translation.
        :return: The translation for the currently specified language setting.
        """
        encapsulate_before, encapsulate_after = self.encapsulate(
            kwargs.get("encapsulate")
        )
        attention: str = self.give_attention(kwargs.get("attention"))
        before, after = self.before_after(kwargs.get("before"), kwargs.get("after"))
        translation: str = self.get(key)
        return "".join(
            [
                attention,
                encapsulate_before,
                before,
                translation.format(*args),
                after,
                encapsulate_after,
            ]
        )
