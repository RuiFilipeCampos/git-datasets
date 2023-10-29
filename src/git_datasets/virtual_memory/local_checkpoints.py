""" TODO """

from typing import final, Iterator
from git_datasets.virtual_memory.abstract import (
    VirtualMemory, RelativePath, AllowedTypes, FileInterface
)

from contextlib import contextmanager
import os

__all__ = ["LocalCheckpoinstVM"]

AbsolutePath = str


class LocalParquetFile(FileInterface):
    """ TODO """

    def __init__(self, path: AbsolutePath):
        self.path = path


    def set_schema(self, desired_schema: dict[str, AllowedTypes]) -> None:
        """ TODO """

    def insert(self) -> None:
        """ TODO """


    def delete(self) -> None:
        """ TODO """


    def alter(self) -> None:
        """ TODO """

    def select(self) -> None:
        """ TODO """

    def close(self):
        """ TODO """

    def save(self):
        """ TODO """

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

    def delete(self, path: RelativePath) -> None:
        """ TODO """

        path = self._make_absolute(path)
        os.remove(path)


    def exists(self, path: RelativePath) -> bool:
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
        return

        # path = self._make_absolute(path)

    def pull(self, path: RelativePath) -> None:
        """ TODO """
        return
    

        # path = self._make_absolute(path)


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

