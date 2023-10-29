""" Implements git hooks. """

from git_datasets.virtual_memory.abstract import VirtualMemory
from git_datasets.types import DecoratedClass
from git_datasets.commands import get_git_current_commit_hash
from git_datasets.interpreter import apply_transforms

RelativePath = str




class GitHooks:
    """ Implements the git strategy. """

    _cls: DecoratedClass
    _virtual_memory: VirtualMemory
    _commit_path: RelativePath
    _commit_exists: bool

    def __init__(self, cls: DecoratedClass, virtual_memory: VirtualMemory):
        """ Operations common to every git-hook """

        self._cls = cls
        self._virtual_memory = virtual_memory
        self._commit_path = f"commits/{get_git_current_commit_hash()}"
        self._commit_exists = self._virtual_memory.exists(self._commit_path)

    def pre_commit(self) -> None:
        """ Pre commit dataset. """

        apply_transforms(self._cls, self._virtual_memory, "current")

    def post_commit(self) -> None:
        """ Pre commit dataset. """

        if self._commit_exists:
            raise RuntimeError("This has been commited already.")

        self._virtual_memory.move("current", self._commit_path)

    def pull(self) -> None:
        """ TODO """

        if self._commit_exists:
            return

        self._virtual_memory.pull(self._commit_path)

    def push(self) -> None:
        """ TODO """

        if not self._commit_exists:
            raise RuntimeError("This has not been commited yet.")

        self._virtual_memory.push(self._commit_path)
