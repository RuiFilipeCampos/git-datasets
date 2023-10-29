""" Repository for all the types used in the codebase. """

from functools import wraps
from typing import Callable, get_type_hints, Any, Unpack, TypeVar
from git_datasets.exceptions import InvalidInputType
from enum import Enum
from typing import TypeAlias

# decorators

DecoratedClass: TypeAlias = type
Decorator: TypeAlias = Callable[[DecoratedClass], DecoratedClass]

# paths 

PathStr: TypeAlias = str
RelativePath: TypeAlias = str
AbsolutePath: TypeAlias = str
SQLCmdStr: TypeAlias = str

class SQLType(Enum):
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    REAL = "REAL"
    BLOB = "BLOB"
    NULL = "NULL"

PySchema: TypeAlias = type[int] | type[str]
FieldNameStr: TypeAlias = str

T = TypeVar("T")

Schema: TypeAlias = dict[FieldNameStr, T]
DatasetSQLSchema: TypeAlias = Schema[SQLType]
DatasetPySchema: TypeAlias = Schema[PySchema]

class Action(type):
    """ Actions for row transformations. """

    class Insert(type):
        """ Add data to the dataset. """

    class Delete(type):
        """ Delete data from the dataset. """

    class Alter(type):
        """ Change data. """


AnyFunction: TypeAlias = Callable[..., Any]

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

