# Built-ins
from re import split
from os.path import splitext


def parse_key(key: str) -> list[str]:
    """Break up key into a list seperated by dots."""
    return split(r"\.", key)


def get_file_extension(filename: str) -> str:
    return splitext(filename)[1][1:]


def csv_to_list(list_string: str) -> list[str]:
    return [element.strip() for element in list_string.split(",")]
