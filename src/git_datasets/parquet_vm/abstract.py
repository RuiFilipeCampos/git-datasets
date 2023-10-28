
from abc import ABC, abstractmethod
from typing import Protocol, Any, Literal, final

RelativePath = str
AllowedTypes = type[int] | type[str] | type[float]

class Operation(Protocol):
    """ Describes a data operation. """

    kind: Literal["INSERT", "DELETE", "ALTER"]
    data: Any

class ParquetVirtualMemory(ABC):
    """ TODO """

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def set_schema(self, desired_schema: dict[str, AllowedTypes]) -> None:
        """ TODO """

    @abstractmethod
    def add_operation(self, operation: Operation) -> None:
        """ TODO """

    @abstractmethod
    def write(self, path: RelativePath) -> None:
        """ TODO """

    @abstractmethod
    def move(self, src: RelativePath, dest: RelativePath) -> None:
        """ TODO """

    @abstractmethod
    def push(self, path: RelativePath) -> None:
        """ TODO """

    @abstractmethod
    def pull(self, path: RelativePath) -> None:
        """ TODO """