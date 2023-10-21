""" TODO: docstring """

from .types import DatasetSchema, SQLCmdStr, SQLTypeStrLit

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
            DROP COLUMN {field_name};
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
