""" Repository for all the types used in the codebase. """

from typing import Callable, Any, TypeVar, Annotated
from enum import Enum
from collections import OrderedDict

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

Schema = OrderedDict[FieldNameStr, T]
DatasetSQLSchema = Schema[SQLType]
DatasetPySchema = Schema[PyType]
SHA1Hash = str
GitCommitHash = SHA1Hash