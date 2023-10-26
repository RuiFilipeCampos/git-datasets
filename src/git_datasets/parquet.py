""" TODO """

import os.path
from contextlib import contextmanager
from abc import ABC, abstractmethod
from typing import Iterator

from git_datasets.config import DatasetRunConfig
from git_datasets.logging import get_logger

logger = get_logger(__name__)

class ParquetFileInterface(ABC):
    """ Interface that all parquet handlers must implement. """

    @classmethod
    @contextmanager
    @abstractmethod
    def open(cls, config: DatasetRunConfig) -> Iterator["ParquetFileInterface"]:
        """ Handle connection to the parquet database """

    @abstractmethod
    def set_schema(self, desired_schema: dict[str, object]) -> None:
        """ TODO """

class ParquetFileHandler(ParquetFileInterface):
    """ TODO """

    def __init__(self, parquet_file: str):
        """ TODO """

        self.parquet_file = parquet_file

        import pyarrow as pa

        self.python_to_arrow = {
            str: pa.string(),
            int: pa.int32(),
        }

        if not os.path.exists(parquet_file):
            logger.debug("Parquet file does not exist")


    @classmethod
    @contextmanager
    def open(cls, config: DatasetRunConfig) -> Iterator["ParquetFileHandler"]:

        try:
            yield cls(config.parquet_file)
        finally:
            ...


    def _get_schema(self) -> dict:
        """ TODO """
        if not os.path.exists(self.parquet_file):
            logger.debug("Parquet file does not exist")
            return {}
        return {}

    def set_schema(self, desired_schema: dict[str, object]) -> None:
        """ TODO """

        current_schema = self._get_schema()
        logger.debug("Current schema: %s", current_schema)

        for field_name, field_type in current_schema.items():
            if field_name not in desired_schema:
                self._delete_field(field_name)
                continue

            if not desired_schema[field_name] != field_type:
                new_field_type = desired_schema[field_name]
                self._alter_field_type(field_name, new_field_type)
                continue

        for field_name, field_type in desired_schema.items():
            if field_name not in current_schema:
                self._add_field(field_name, field_type)
                continue

            if not current_schema[field_name] != field_type:
                self._alter_field_type(field_name, field_type)
                continue

    def _delete_field(self, field_name: str) -> None:
        """ TODO """
        logger.debug("Deleting field: '%s'", field_name)

    def _add_field(self, field_name: str, field_type: object) -> None:
        """ TODO """

        logger.debug("Adding field '%s' of type '%s'", field_name, field_type)

    def _alter_field_type(self, field_name: str, field_type: object) -> None:
        """ TODO """
        logger.debug("Altering field type: '%s' to '%s'", field_name, field_type)
