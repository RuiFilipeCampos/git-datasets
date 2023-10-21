""" git_operations.py

This module provides utility functions to facilitate interactions with Git repositories.
It contains operations to retrieve metadata and perform certain tasks related to Git.
It leverages the command-line interface of Git to achieve these functionalities.
"""

import subprocess
import os

def get_git_root_path() -> str | None:
    """ Retrieve the root path of the current Git repository. """

    try:
        commands = ['git', 'rev-parse', '--show-toplevel']
        base_path = subprocess               \
                    .check_output(commands)  \
                    .strip()                 \
                    .decode('utf-8')

        return base_path
    except subprocess.CalledProcessError:
        return None
