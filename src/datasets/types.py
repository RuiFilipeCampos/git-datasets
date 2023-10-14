""" TODO: docstring """

from typing import Literal, Callable


# Application types and constants
DecoratedClass = type
SQLCmdStr = str
PathStr = str
FieldNameStr = str

Decorator = Callable[[DecoratedClass], DecoratedClass]

DiffSchema = dict[Literal["add", "remove"], list[FieldNameStr]]

SQLTypeStrLit = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]

DatasetSchema = dict[FieldNameStr, SQLTypeStrLit]
