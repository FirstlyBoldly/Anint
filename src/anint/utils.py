# Built-ins
from re import split


def parse_key(key: str) -> list[str]:
    """Break up key into a list seperated by dots."""
    return split(r"\.", key)
