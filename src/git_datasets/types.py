""" Repository for all the types used in the codebase. """

from typing import Callable, Any, TypeVar, Annotated
from enum import Enum
from typing import TypeAlias


S = TypeVar("S")
T = TypeVar("T")
U = TypeVar("U", bound=Callable)

AnyFunction = Callable[..., Any]
SingleArgFunction = Callable[[S], T]
TypeCheckedArgs = Annotated[U, "Has been validated at runtime."]

# decorators

# NOTE The class decorated with "@dataset".

AnnotatedClass = type
DecoratedClass = type

Decorator = SingleArgFunction[DecoratedClass, DecoratedClass]

# paths 

PathStr = str
RelativePath = str
AbsolutePath = str
SQLCmdStr = str

class SQLType(Enum):
    """ SQL Types supported by duckdb. """

    TEXT = "TEXT"
    INTEGER = "INTEGER"
    REAL = "REAL"
    BLOB = "BLOB"
    NULL = "NULL"

class PyType(Enum):
    """ Python types that are allowed in the schema."""

    STR = str
    INT = int
    FLOAT = float


FieldNameStr = str

Schema = dict[FieldNameStr, T]
DatasetSQLSchema = Schema[SQLType]
DatasetPySchema = Schema[PyType]

class Action(Enum):
    """ Actions for row transformations. """

    class Insert(type):
        """ Add data to the dataset. """

    class Delete(type):
        """ Delete data from the dataset. """

    class Alter(type):
        """ Change data. """

    NoAction = None





SHA1Hash = str
GitCommitHash = SHA1Hash