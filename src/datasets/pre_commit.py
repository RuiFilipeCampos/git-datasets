"""TODO: Docstring"""

def pre_commit(*args, **kwargs):
    raise NotImplementedError



"""

# note: _get* are pure functions, no side effects
# while _modify* is the opposite

desired_schema = _get_desired_schema(cls)
current_schema = _get_current_schema(cursor, cls.__name__)
diff_schema = _get_schema_diff(current_schema, desired_schema)
del current_schema, desired_schema

_modify_sql_database(cursor, diff_schema)
_modify_data_directory(data_dir, diff_schema)
_modify_history(data_dir)

_modify_class(cls)


# logic used by @dataset, all function definitions appear in the same order
def _get_desired_schema(cls: DecoratedClass) -> DatasetSchema:
    \"""
    Extracts the desired schema from the provided class based on its annotations.
    \"""

    field_to_type_mapping = cls.__annotations__.items()

    return {
        field_name: PYTHON_TO_SQLITE3[field_type]
        for field_name, field_type 
        in field_to_type_mapping
    }

def _get_current_schema(cursor: Cursor, table_name: str) -> DatasetSchema:
    ""
    Queries and retrieves the current schema of the specified table.
    ""

    schema_query = SQLCommandGenerator.schema_query_cmd(table_name)
    cursor.execute(schema_query)
    logger.debug("Executed SQL: %s", schema_query)
    return { column[1]: column[2] for column in cursor.fetchall() }


def _get_schema_diff(
    current_schema: DatasetSchema, desired_schema: DatasetSchema
) -> DiffSchema:
    ""
    Compute the difference between the desired schema and the current schema.
    ""

    print(current_schema)
    print(desired_schema)
    return {}


def _modify_sql_database(cursor: Cursor, diff_schema: dict) -> None:
    ""
    Apply schema changes based on the computed difference.
    ""
    print(cursor)
    print(diff_schema)


def _modify_data_directory(data_dir: PathStr, diff_schema: dict) -> None:
    ""
    Apply directory changes based on the computed difference.
    ""
    print(data_dir)
    print(diff_schema)

def _modify_class(cls: DecoratedClass) -> DecoratedClass:
    ""
    Modify the class to provide additional functionality or 
    bind it to the dataset.
    ""

    print(cls)
    return cls

def _modify_history(data_dir: PathStr):
    ...
    # commit this file
    # commit the data



"""