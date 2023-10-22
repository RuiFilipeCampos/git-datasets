""" config.py

Configuration and utilities for dataset run settings in the context of a git repository.

"""

import os
import sys
from dataclasses import dataclass
from contextlib import contextmanager
from typing import ContextManager, Type

from git_datasets.commands import get_git_root_path
from git_datasets.logging import get_logger

logger = get_logger(__name__)

@dataclass
class DatasetRunConfig:
    """ Configuration for Dataset runs within a git repository context. """

    dataset_name: str

    # Path to the script being run.
    main_script_path: str = os.path.abspath(sys.argv[0])

    # Root of the git repository
    repository_root: str = get_git_root_path()

    # Path to the hidden directory
    hidden_dir: str = os.path.join(repository_root, ".gitdatasets")

    parquet_file: str = os.path.join(hidden_dir, "db.parquet")


    @classmethod
    @contextmanager
    def init(
        cls: Type["DatasetRunConfig"],
        *,
        dataset_name: str,
    ) -> ContextManager["DatasetRunConfig"]:
        """ Context manager to initialize and manage a `DatasetRunConfig` 
        instance. """

        self = cls(dataset_name=dataset_name)

        if not os.path.exists(self.hidden_dir):
            os.mkdir(self.hidden_dir)
            logger.info("Created hidden configuration folder at %s.", self.hidden_dir)

        try:
            yield self
        finally:
            # self.spark.stop()
            logger.debug("Exited git-datasets.")
