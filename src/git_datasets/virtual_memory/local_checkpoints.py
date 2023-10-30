""" Implements the local checkpoints strategy for managing parquet files. """

import os
from contextlib import contextmanager
from typing import final, Iterator, Final, Protocol, Any

from duckdb import (
    DuckDBPyConnection, # for type hinting
    connect # for generating a `DuckDBPyConnection` instance
)

from git_datasets.types import RelativePath, AbsolutePath, DatasetSQLSchema, SQLType
from git_datasets.logging import get_logger
from git_datasets.commands import get_git_root_path
from git_datasets.virtual_memory.abstract import (
    VirtualMemory, AllowedPythonTypes, FileInterface
)

logger = get_logger(__name__)


__all__ = ["LocalCheckpoinstVM"]

TypeMap = dict[type, SQLType]
FieldSpec = tuple[object, str, SQLType]


class LocalParquetFile(FileInterface):
    """ TODO """

    _path: AbsolutePath
    _conn: DuckDBPyConnection
    _file_exists: bool

    TYPE_MAP: Final[TypeMap] = {
        int: "INTEGER",
        str: "VARCHAR",
    }

    def __init__(self, path: AbsolutePath):
        self._path = path
        self._conn = connect(database=':memory:', read_only=False)
        self._file_exists = os.path.exists(path)
        if self._file_exists:
            self._conn.execute(f"""
                CREATE TABLE dataset AS SELECT *
                FROM parquet_scan('{self._path}');
            """)

    def set_schema(self, desired_schema: dict[str, AllowedPythonTypes]) -> None:
        """ Set the database schema. """

        desired_sql_schema = {
            field_n: self.TYPE_MAP[field_t]
            for field_n, field_t in desired_schema.items()
        }

        if not self._file_exists:
            sql = 'CREATE TABLE dataset ('
            for field_n, field_t in desired_sql_schema.items():
                sql += f'{field_n} {field_t},'
            sql += ')'
            self._conn.execute(sql)
            return

        connection = self._conn.execute("PRAGMA table_info(dataset);")
        result: list[FieldSpec] = connection.fetchall()
        current_sql_schema: DatasetSQLSchema = { field[1]: field[2] for field in result }

        logger.debug("Current schema: %s", current_sql_schema)
        logger.debug("Current schema: %s", desired_sql_schema)

        for field_name, field_type in current_sql_schema.items():
            if field_name not in desired_sql_schema:
                self._conn.execute(f"ALTER TABLE dataset DROP COLUMN {field_name}")
                continue

            if desired_sql_schema[field_name] != field_type:
                new_field_type = desired_sql_schema[field_name]
                self._conn.execute(f"ALTER TABLE dataset DROP COLUMN {field_name}")
                self._conn.execute(f"ALTER TABLE dataset  ADD COLUMN {field_name} {new_field_type}")
                continue

        for field_name, field_type in desired_sql_schema.items():
            if field_name not in current_sql_schema:
                self._conn.execute(f"ALTER TABLE dataset ADD COLUMN {field_name} {field_type}")
                continue

            if current_sql_schema[field_name] != field_type:
                self._conn.execute(f"ALTER TABLE dataset DROP COLUMN {field_name}")
                self._conn.execute(f"ALTER TABLE dataset  ADD COLUMN {field_name} {field_type}")
                continue

    def insert(self) -> None:
        """ TODO """

    def delete(self) -> None:
        """ TODO """

    def alter(self) -> None:
        """ TODO """

    def select(self) -> None:
        """ TODO """

    def close(self) -> None:
        """ Removes the tables from memory. """

        self._conn.close()

    def save(self) -> None:
        """ Saves the in-memory table to the parquet file. """

        self._conn.execute(f"""
            COPY dataset TO '{self._path}' (FORMAT 'PARQUET')
        """)

@final
class LocalCheckpoinstVM(VirtualMemory):
    """ Implements local parquet checkpoints strategy.
     
        - This strategy creates a parquet checkpoint for each commit
        - Commits do not get pushed or pulled from any remote.
    """

    path_prefix: str

    def __init__(self) -> None:
        """ TODO """
        git_root = get_git_root_path()
        self.path_prefix = os.path.join(git_root, ".gitdatasets")
        os.makedirs(self.path_prefix, exist_ok=True)

    def _make_absolute(self, path: RelativePath) -> AbsolutePath:
        """ Compute absolute path. """
        return os.path.join(self.path_prefix, path)

    def delete(self, path: RelativePath) -> None:
        """ Remove file. """
        path = self._make_absolute(path)
        os.remove(path)

    def exists(self, path: RelativePath) -> bool:
        """ Check if file exists. """

        path = self._make_absolute(path)
        return os.path.exists(path)

    def move(self, src: RelativePath, dest: RelativePath) -> None:
        """ Move file from `src` to `dest`. """

        src = self._make_absolute(src)
        dest = self._make_absolute(dest)
        dest_parent = os.path.dirname(dest)
        os.makedirs(dest_parent, exist_ok=True)
        os.rename(src, dest)

    def push(self, path: RelativePath) -> None:
        """ Push file to remote - not implemented in local strategy. """
        return

    def pull(self, path: RelativePath) -> None:
        """ Pull file from remote - not implemented in local strategy. """
        return

    @contextmanager
    def open(self, path: RelativePath) -> Iterator[LocalParquetFile]:
        """ Open a parquet file. """

        path = self._make_absolute(path)
        file = LocalParquetFile(path)
        
        try:
            yield file
        finally:
            file.save()
            file.close()

