""" TODO """

from typing import final
from git_datasets.virtual_memory.abstract import (
    VirtualMemory, RelativePath, AllowedTypes, Operation
)
import os

__all__ = ["LocalCheckpoinstVM"]

AbsolutePath = str

@final
class LocalCheckpoinstVM(VirtualMemory):
    """ TODO """

    path_prefix: str

    def __init__(self) -> None:
        """ TODO """

        self.path_prefix = "/workspaces/git-datasets/.gitdatasets"

    def _make_absolute(self, path: RelativePath) -> AbsolutePath:
        """ TODO """
        return os.path.join(self.path_prefix, path)

    def load(self, path: RelativePath) -> None:
        """ TODO """

        path = self._make_absolute(path)

    def exists(self, path: RelativePath) -> None:
        """ TODO """

        path = self._make_absolute(path)
        return os.path.exists(path)

    def move(self, src: RelativePath, dest: RelativePath) -> None:
        """ TODO """

        src = self._make_absolute(src)
        dest = self._make_absolute(dest)
        os.rename(src, dest)


    def push(self, path: RelativePath) -> None:
        """ TODO """

        path = self._make_absolute(path)

    def pull(self, path: RelativePath) -> None:
        """ TODO """

        path = self._make_absolute(path)

    def write(self, path: RelativePath) -> None:
        """ TODO """

        path = self._make_absolute(path)

    def set_schema(self, desired_schema: dict[str, AllowedTypes]) -> None:
        """ TODO """

    def add_operation(self, operation: Operation) -> None:
        """ TODO """
