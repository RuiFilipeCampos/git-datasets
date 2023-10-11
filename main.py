"""
Prototype for the datasets project.
"""

import sqlite3
from sqlite3 import Cursor
from contextlib import closing
import uuid
from typing import Literal, Callable, get_type_hints
import logging
from functools import wraps

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("datasets")



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
                msg = f"Argument {name} should be of type {expected_type}, "
                msg += f"but got {type(value)} instead."
                raise TypeError(msg)

        return func(*args, **kwargs)
    return wrapper


# Application types and constants
DecoratedClass = type
SQLTypeStrLit = Literal["TEXT", "INTEGER"]
FieldNameStr = str
SQLCmdStr = str
PathStr = str
DatasetSchema = dict[FieldNameStr, SQLTypeStrLit]

Decorator = Callable[
    [DecoratedClass],
    DecoratedClass
]

DiffSchema = dict[
    Literal["add", "remove"],
    list[FieldNameStr]
]

PYTHON_TO_SQLITE3: dict[type, SQLTypeStrLit] = {
    str: "TEXT",
    int: "INTEGER",
}




class SQLCommandGenerator:
    """
    A utility class to generate SQL commands for table manipulation
    based on specified schemas and table configurations.
    """

    @staticmethod
    def create_table_cmd(table_name: str, schema: DatasetSchema) -> SQLCmdStr:
        """
        Generates a SQL command to create a new table based on the provided schema.
        """
        schema_fields = schema.items()
        columns = ", ".join(
            f"{field_name} {field_type}"
            for field_name, field_type
            in schema_fields
        )

        return f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columns}
            );
        """

    @staticmethod
    def schema_query_cmd(table_name: str) -> SQLCmdStr:
        """Queries the schema of the specified table."""
        return f"PRAGMA table_info({table_name});"

    @staticmethod
    def del_field_cmd(table_name: str, field_name: str) -> SQLCmdStr:
        """Generates a command to rename a field, effectively
        "deleting" it by marking as deleted."""
        return f"""
            ALTER TABLE {table_name} 
            RENAME COLUMN {field_name} 
            TO deleted_{field_name}_{uuid.uuid4().hex};
        """

    @staticmethod
    def add_field_cmd(
        table_name: str,
        field_name: str,
        field_type: SQLTypeStrLit,
    ) -> SQLCmdStr:
        """Generates a command to add a new field to the specified table."""

        return f"""
            ALTER TABLE {table_name}
            ADD COLUMN {field_name} {field_type};
        """


def dataset(
    sql_file: PathStr = "./dataset.sqlite",
    data_dir: PathStr = "./dataset",
) -> Decorator:
    """
    A decorator to manage the lifecycle of the SQLite connection 
    and initialize a dataset with the provided schema.
    """

    def decorator(cls: DecoratedClass) -> DecoratedClass:
        with closing(sqlite3.connect(sql_file)) as conn:
            cursor = conn.cursor()
            return _decorate_class(cls, cursor, data_dir)
    return decorator


def _decorate_class(
    cls: DecoratedClass, cursor: Cursor, data_dir: PathStr
) -> DecoratedClass:

    # note: _get* are pure functions, no side effects
    # while _modify* is the opposite

    desired_schema = _get_desired_schema(cls)
    current_schema = _get_current_schema(cursor, cls.__name__)
    diff_schema = _get_schema_diff(current_schema, desired_schema)
    del current_schema, desired_schema

    _modify_sql_database(cursor, diff_schema)
    _modify_data_directory(data_dir, diff_schema)

    return _modify_class(cls)


# logic used by @dataset, all function definitions appear in the same order
def _get_desired_schema(cls: DecoratedClass) -> DatasetSchema:
    """
    Extracts the desired schema from the provided class based on its annotations.
    """

    field_to_type_mapping = cls.__annotations__.items()

    return {
        field_name: PYTHON_TO_SQLITE3[field_type]
        for field_name, field_type 
        in field_to_type_mapping
    }

def _get_current_schema(cursor: Cursor, table_name: str) -> DatasetSchema:
    """
    Queries and retrieves the current schema of the specified table.
    """

    schema_query = SQLCommandGenerator.schema_query_cmd(table_name)
    cursor.execute(schema_query)
    logger.debug("Executed SQL: %s", schema_query)

    return { column[1]: column[2] for column in cursor.fetchall() }


def _get_schema_diff(current_schema: DatasetSchema, desired_schema: DatasetSchema) -> DiffSchema:
    """
    Compute the difference between the desired schema and the current schema.
    """

    print(current_schema)
    print(desired_schema)
    return {}


def _modify_sql_database(cursor: Cursor, diff_schema: dict) -> None:
    """
    Apply schema changes based on the computed difference.
    """
    print(cursor)
    print(diff_schema)


def _modify_data_directory(data_dir: PathStr, diff_schema: dict) -> None:
    """
    Apply directory changes based on the computed difference.
    """
    print(data_dir)
    print(diff_schema)

def _modify_class(cls: DecoratedClass) -> DecoratedClass:
    """
    Modify the class to provide additional functionality or 
    bind it to the dataset.
    """

    print(cls)
    return cls
