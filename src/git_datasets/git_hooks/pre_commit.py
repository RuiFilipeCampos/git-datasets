"""
This module provides functionality to shape the datasets prior to committing their index.py file.

This code is executed when:

```
python index.py --pre-commit
```

is executed. Which itself is called as a git hook by `git commit index.py`. 

It focuses on:
1. Adjusting the database schema to match a desired state. 
   This includes querying the current schema, computing differences, 
   and then applying those differences both to the SQL database 
   and to the corresponding data directory structure.
2. Handling row changes. 


Note:
- The functions prefixed with `_get` are pure and have no side effects, 
  while those prefixed with `_modify` perform changes to their respective targets.
"""

from git_datasets.types import DatasetSchema, DecoratedClass, DiffSchema, PathStr


# TODO: fix this
Cursor = None


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


def _get_schema_diff(
    current_schema: DatasetSchema, desired_schema: DatasetSchema
) -> DiffSchema:
    """
    Compute the difference between the desired schema and the current schema.
    """

    print(current_schema)
    print(desired_schema)
    return {}


def _modify_sql_database_schema(cursor: Cursor, diff_schema: DiffSchema) -> None:
    """
    Apply schema changes based on the computed difference.
    """
    print(cursor)
    print(diff_schema)


def _modify_data_directory_structure(data_dir: PathStr, diff_schema: DiffSchema) -> None:
    """
    Apply directory changes based on the computed difference.
    """
    print(data_dir)
    print(diff_schema)


def pre_commit(cls, *args, **kwargs) -> None:
    """ Pre commit dataset. """

    # note: _get* are pure functions, no side effects
    # while _modify* is the opposite

    # handle horizontal (schema) changes
    desired_schema = _get_desired_schema(cls)
    current_schema = _get_current_schema(cursor, cls.__name__)
    diff_schema = _get_schema_diff(current_schema, desired_schema)
    del current_schema, desired_schema

    if len(diff_schema) != 0:
        _modify_sql_database_schema(cursor, diff_schema)
        _modify_data_directory_structure(data_dir, diff_schema)

    # handle vertical (row) changes

    ...
    



