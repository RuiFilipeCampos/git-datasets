""" TODO """

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