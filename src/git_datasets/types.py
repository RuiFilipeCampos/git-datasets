""" Repository for all the types used in the codebase. """

from functools import wraps
from typing import Literal, Callable, get_type_hints
from git_datasets.exceptions import InvalidInputType

# Application types and constants
DecoratedClass = type
SQLCmdStr = str
PathStr = str
FieldNameStr = str

RelativePath = str
AbsolutePath = str

Decorator = Callable[[DecoratedClass], DecoratedClass]

DiffSchema = dict[Literal["add", "remove"], list[FieldNameStr]]

SQLTypeStrLit = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]

DatasetSchema = dict[FieldNameStr, SQLTypeStrLit]


class Action(type):
    """ Actions for row transformations. """

    class Insert(type):
        """ Add data to the dataset. """

    class Delete(type):
        """ Delete data from the dataset. """

    class Alter(type):
        """ Change data. """



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
