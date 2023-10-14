"""
Entrypoint for the git-datasets package.
"""

import sqlite3
from contextlib import closing
import logging
import argparse
import os.path

from .types import DecoratedClass, Decorator
from .pre_commit import pre_commit
from .pull import pull
from .push import push
from .checkout import checkout


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("datasets")


def dataset(*, remote: str) -> Decorator:
    """
    This decorator parses command line arguments and feeds
    the results to the chosen action.
    """

    def decorator(cls: DecoratedClass) -> DecoratedClass:
        if __name__ == "__main__":

            # parse arguments
            parser = argparse.ArgumentParser()
            parser.add_argument("path", help="Path to the root folder.")
            actions = [ "--pre-commit", "--pull", "--push", "--post-checkout" ]
            group = parser.add_mutually_exclusive_group(required=True)
            for action in actions:
                group.add_argument(action, action="store_true")
            parser.parse_args()

            data_dir = os.path.join(parser.path, "data")
            sql_file = os.path.join(parser.path, "dataset.sqlite")

            # choose action 
            if parser.pre_commit:
                pre_commit(cls, data_dir, sql_file, remote)
            elif parser.pull:
                pull(cls, data_dir, sql_file, remote)
            elif parser.push:
                push(cls, data_dir, sql_file, remote)
            elif parser.post_checkout:
                checkout(cls, data_dir, sql_file, remote)

        return cls
    return decorator
