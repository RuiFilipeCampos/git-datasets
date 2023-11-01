""" Defines the interface that all virtual memory implementations must
conform to in order to fit into the codebase. """

from abc import ABC, abstractmethod
from typing import Iterator
from contextlib import contextmanager

from git_datasets.types import RelativePath, DatasetPySchema


class FileInterface(ABC):
    """ Provides a virtual interface to edit
     a parquet file. """

    @abstractmethod
    def set_schema(self, desired_schema: DatasetPySchema) -> None:
        """ Set the schema. """

    @abstractmethod
    def insert(self, fields: list[str], data: list) -> None:
        """ Insert a new row. """

    @abstractmethod
    def delete(self) -> None:
        """ Delete an existing row. """

    @abstractmethod
    def alter(self) -> None:
        """ Modify a given row. """

    @abstractmethod
    def select(self) -> None:
        """ Select a row or column. """


class VirtualMemory(ABC):
    """ Provides a virtual file system. """

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def move(self, src: RelativePath, dest: RelativePath) -> None:
        """ TODO """

    @abstractmethod
    def delete(self, path: RelativePath) -> None:
        """ TODO """

    @abstractmethod
    def exists(self, path: RelativePath) -> bool:
        """ TODO """

    @abstractmethod
    def push(self, path: RelativePath) -> None:
        """ TODO """

    @abstractmethod
    def pull(self, path: RelativePath) -> None:
        """ TODO """

    @abstractmethod
    @contextmanager
    def open(self, path: RelativePath) -> Iterator[FileInterface]:
        """ TODO """
