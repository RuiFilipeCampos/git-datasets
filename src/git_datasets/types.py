""" TODO: docstring """

from typing import Literal, Callable, get_type_hints
from .exceptions import InvalidInputType
from functools import wraps


# Application types and constants
DecoratedClass = type
SQLCmdStr = str
PathStr = str
FieldNameStr = str

Decorator = Callable[[DecoratedClass], DecoratedClass]

DiffSchema = dict[Literal["add", "remove"], list[FieldNameStr]]

SQLTypeStrLit = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]

DatasetSchema = dict[FieldNameStr, SQLTypeStrLit]


def validate_arguments(func: Callable) -> Callable:
    """ Runtime validation of function arguments. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        for name, value in kwargs.items():
            expected_type = hints.get(name)

            if expected_type is None:
                continue

            if not isinstance(value, expected_type):
                raise InvalidInputType(name, expected_type, value)

        return func(*args, **kwargs)
    return wrapper
