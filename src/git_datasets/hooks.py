""" TODO """

from git_datasets.parquet_vm.abstract import ParquetVirtualMemory
from git_datasets.types import DecoratedClass
from git_datasets.commands import get_git_current_commit_hash
from git_datasets.interpreter import cls_to_schema

class GitHooks:
    """ Implements the git strategy. """

    _cls: DecoratedClass
    _parquet_vm: ParquetVirtualMemory
    _commit_parquet_file: str


    def __init__(self, cls: DecoratedClass, parquet_vm: ParquetVirtualMemory):
        """ Operations common to every git-hook """

        self._cls = cls
        self._parquet_vm = parquet_vm
        self._commit_path = f"commits/{get_git_current_commit_hash()}"
        self._commit_exists = self._parquet_vm.exists(self._commit_path)


    def pre_commit(self) -> None:
        """ Pre commit dataset. """

        if self._commit_exists:
            raise RuntimeError("This has been commited already.")

        desired_schema = cls_to_schema(self._cls)
        self._parquet_vm.set_schema(desired_schema)
        self._parquet_vm.write("current")

    def post_commit(self) -> None:
        """ Pre commit dataset. """

        if self._commit_exists:
            raise RuntimeError("This has been commited already.")

        self._parquet_vm.move("current", self._commit_parquet_file)

    def pull(self) -> None:
        """ TODO """

        if self._commit_exists:
            return

        self._parquet_vm.pull(self._commit_parquet_file)

    def push(self) -> None:
        """ TODO """

        if not self._commit_exists:
            raise RuntimeError("This has not been commited yet.")

        self._parquet_vm.push(self._commit_parquet_file)
