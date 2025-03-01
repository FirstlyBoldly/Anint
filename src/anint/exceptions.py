class TranslationError(ValueError):
    """Missing or invalid translation."""

class AnintConfigError(RuntimeError):
    """Invalid configuration."""

class MultipleSameLocaleError(RuntimeError):
    """Multiple files with the same locale."""
