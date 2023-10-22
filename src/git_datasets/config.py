""" config.py

Configuration and utilities for dataset run settings in the context of a git repository.

"""

from dataclasses import dataclass
import os
import sys
from contextlib import contextmanager
from typing import ContextManager, Type

from git_datasets.git_operations import get_git_root_path

@dataclass
class DatasetRunConfig:
    """ Configuration for Dataset runs within a git repository context. """

    # Path to the script being run.
    main_script_path: str = os.path.abspath(sys.argv[0])

    # Root of the git repository
    repository_root: str = get_git_root_path()

    # Path to the hidden directory
    hidden_dir: str = os.path.join(repository_root, ".gitdatasets")


    @classmethod
    @contextmanager
    def init(cls: Type["DatasetRunConfig"]) -> ContextManager["DatasetRunConfig"]:
        """  Context manager to initialize and manage a `DatasetRunConfig` 
        instance. """

        self = cls()

        if not os.path.exists(self.hidden_dir):
            os.mkdir(self.hidden_dir)

        try:
            yield self
        finally:
            ...
            # TODO: cleanup 




