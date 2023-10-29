""" Repository for all the types used in the codebase. """

from functools import wraps
from typing import Callable, get_type_hints, Any, Unpack
from git_datasets.exceptions import InvalidInputType
from enum import Enum

# Application types and constants
type DecoratedClass = type
type Decorator = Callable[[DecoratedClass], DecoratedClass]

type SQLCmdStr = str
type FieldNameStr = str
type PathStr = str
type RelativePath = str
type AbsolutePath = str

class SQLType(Enum):
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    REAL = "REAL"
    BLOB = "BLOB"
    NULL = "NULL"

type PySchema = type[int] | type[str]

type Schema[T] = dict[str, T]
type DatasetSQLSchema = Schema[SQLType]
type DatasetPySchema = Schema[PySchema]

type AnyFunction = Callable[..., Any]

class Action(type):
    """ Actions for row transformations. """

    class Insert(type):
        """ Add data to the dataset. """

    class Delete(type):
        """ Delete data from the dataset. """

    class Alter(type):
        """ Change data. """



def validate_arguments(function: AnyFunction) -> AnyFunction:
    """ Runtime validation of function arguments. """

    @wraps(function)
    def wrapper(*args: Unpack[Any], **kwargs: Unpack[Any]) -> Any:
        hints = get_type_hints(function)
        for name, value in kwargs.items():
            expected_type = hints.get(name)

            if expected_type is None:
                continue

            if not isinstance(value, expected_type):
                raise InvalidInputType(name, expected_type, value)

        return function(*args, **kwargs)
    return wrapper
