""" Defines the interface that all virtual memory implementations must
conform to in order to fit into the codebase. """

from abc import ABC, abstractmethod
from typing import Protocol, Any, Literal, Iterator
from contextlib import contextmanager

RelativePath = str
AllowedTypes = type[int] | type[str] | type[float]


class FileInterface(ABC):
    """ Provides a virtual interface to edit
     a parquet file. """

    @abstractmethod
    def set_schema(self, desired_schema: dict[str, AllowedTypes]) -> None:
        """ TODO """

    @abstractmethod
    def insert(self) -> None:
        """ TODO """

    @abstractmethod
    def delete(self) -> None:
        """ TODO """

    @abstractmethod
    def alter(self) -> None:
        """ TODO """

    @abstractmethod
    def select(self) -> None:
        """ TODO """


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
