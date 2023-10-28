
from typing import final
from git_datasets.parquet_vm.abstract import (
    ParquetVirtualMemory, RelativePath, AllowedTypes, Operation
)


@final
class LocalParquetVM(ParquetVirtualMemory):
    """ TODO """

    def __init__(self) -> None:
        """ TODO """

    def set_schema(self, desired_schema: dict[str, AllowedTypes]) -> None:
        """ TODO """

    def add_operation(self, operation: Operation) -> None:
        """ TODO """

    def write(self, path: RelativePath) -> None:
        """ TODO """

    def move(self, src: RelativePath, dest: RelativePath) -> None:
        """ TODO """

    def push(self, path: RelativePath) -> None:
        """ TODO """

    def pull(self, path: RelativePath) -> None:
        """ TODO """
