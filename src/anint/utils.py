# Built-ins
from re import split
from os.path import split

def parse_key(key: str) -> list[str]:
    """Break up key into a list seperated by dots."""
    return split(r"\.", key)


def get_file_extension(filename: str) -> str:
    return split(filename)[1][1:]
