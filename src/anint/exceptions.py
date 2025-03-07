"""Exceptions for Anint."""

# Built-ins
from typing import Optional


class TranslationError(ValueError):
    """Missing or invalid translation."""

    def __init__(
        self, key: Optional[str], override_warning: Optional[str] = None
    ) -> None:
        """Create and return a new TranslationError instance."""
        if not override_warning:
            override_warning = "{key} is not a invalid translation key.".format(key=key)

        super(TranslationError, self).__init__(override_warning)


class AnintConfigError(RuntimeError):
    """Invalid configuration."""


class MultipleSameLocaleError(RuntimeError):
    """Multiple files with the same locale."""
