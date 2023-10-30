""" Repository for all the types used in the codebase. """

from typing import Callable, Any, TypeVar
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

SHA1Hash = str
GitCommitHash = SHA1Hash