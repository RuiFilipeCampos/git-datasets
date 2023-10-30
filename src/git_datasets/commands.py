""" 
Interactions with the command line
"""

import subprocess

from git_datasets.types import AbsolutePath, GitCommitHash
from git_datasets.logging import get_logger

logger = get_logger(__name__)

def get_git_root_path() -> AbsolutePath:
    """ Retrieve the root path of the current Git repository. """

    try:
        commands = ['git', 'rev-parse', '--show-toplevel']
        base_path = subprocess               \
                    .check_output(commands)  \
                    .strip()                 \
                    .decode('utf-8')

        return base_path
    except subprocess.CalledProcessError:
        logger.error("Couldn't find root of git repository.")
        raise SystemExit

def get_git_current_commit_hash() -> GitCommitHash:
    """ Retrieve the current commit hash of the Git repository. """

    try:
        commands = ['git', 'rev-parse', 'HEAD']
        commit_hash = subprocess              \
                      .check_output(commands) \
                      .strip()                \
                      .decode('utf-8')

        return commit_hash
    except subprocess.CalledProcessError:
        logger.error("Couldn't get the hash of the current commit.")
        raise SystemExit
