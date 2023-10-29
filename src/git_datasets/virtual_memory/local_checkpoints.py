""" Implements the local checkpoints strategy for managing parquet files. """

from contextlib import contextmanager
import os
from typing import final, Iterator, Final

from duckdb import (
    DuckDBPyConnection, # for type hinting
    connect # for generating a `DuckDBPyConnection` instance
)

from git_datasets.types import RelativePath, AbsolutePath
from git_datasets.logging import get_logger
from git_datasets.virtual_memory.abstract import (
    VirtualMemory, AllowedTypes, FileInterface
)
from git_datasets.commands import get_git_root_path


logger = get_logger(__name__)


__all__ = ["LocalCheckpoinstVM"]


class LocalParquetFile(FileInterface):
    """ TODO """

    _path: AbsolutePath
    _conn: DuckDBPyConnection
    _file_exists: bool

    TYPE_MAP: Final[dict] = {
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

    def set_schema(self, desired_schema: dict[str, AllowedTypes]) -> None:
        """ Set the database schema. """

        desired_schema = {
            field: self.TYPE_MAP[field_t]
            for field, field_t in desired_schema.items()
        }

        if not self._file_exists:
            sql = 'CREATE TABLE dataset ('
            for field, field_t in desired_schema.items():
                sql += f'{field} {field_t},'
            sql += ')'
            self._conn.execute(sql)
            return

        current_schema = self.get_schema()

        logger.debug("Current schema: %s", current_schema)
        logger.debug("Current schema: %s", desired_schema)

        for field_name, field_type in current_schema.items():
            if field_name not in desired_schema:
                self._delete_field(field_name)
                continue

            if desired_schema[field_name] != field_type:
                new_field_type = desired_schema[field_name]
                self._alter_field_type(field_name, new_field_type)
                continue

        for field_name, field_type in desired_schema.items():
            if field_name not in current_schema:
                self._add_field(field_name, field_type)
                continue

            if current_schema[field_name] != field_type:
                self._alter_field_type(field_name, field_type)
                continue

    def _delete_field(self, field_name: str) -> None:
        """ Delete a field from the dataset. """
        logger.debug("Deleting field: '%s'", field_name)
        self._conn.execute(f"ALTER TABLE dataset DROP COLUMN {field_name}")

    def _add_field(self, field_name: str, field_type: object) -> None:
        """ Add a field to the dataset. """
        logger.debug("Adding field '%s' of type '%s'", field_name, field_type)
        self._conn.execute(f"ALTER TABLE dataset ADD COLUMN {field_name} {field_type}")

    def _alter_field_type(self, field_name: str, field_type: object) -> None:
        """ Change the field type of a given field of the dataset. """
        logger.debug("Altering field type: '%s' to '%s'", field_name, field_type)
        self._delete_field(field_name)
        self._add_field(field_name, field_type)


    def get_schema(self) -> dict[str, str]:
        """ TODO """

        result = self._conn.execute("PRAGMA table_info(dataset);")
        result = result.fetchall()

        current_schema = {}

        for field in result:
            field_n, field_t = field[1], field[2]
            current_schema[field_n] = field_t

        return current_schema

    def insert(self) -> None:
        """ TODO """

    def delete(self) -> None:
        """ TODO """

    def alter(self) -> None:
        """ TODO """

    def select(self) -> None:
        """ TODO """

    def close(self):
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

