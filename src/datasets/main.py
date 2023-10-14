"""
Entrypoint for the git-datasets package.
"""

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
    This decorator serves a twofold purpose:

    1. (write) When executed directly, it acts as a command-line 
    utility tailored for git hooks, parsing arguments
    and triggering the appropriate actions.

    2. (read-only) When used within a package, it decorates classes,
    augmenting or modifying their behavior without 
    directly altering the dataset.
    """

    def decorator(cls: DecoratedClass) -> DecoratedClass:
        if __name__ == "__main__": # write mode

            # parse arguments
            parser = argparse.ArgumentParser()
            parser.add_argument("path", help="Path to the root folder.")
            actions = [ "--pre-commit", "--pull", "--push", "--post-checkout" ]
            group = parser.add_mutually_exclusive_group(required=True)
            for action in actions:
                group.add_argument(action, action="store_true")
            args = parser.parse_args()

            data_dir = os.path.join(args.path, "data")
            sql_file = os.path.join(args.path, "dataset.sqlite")

            # choose action 
            if args.pre_commit:
                pre_commit(cls, data_dir, sql_file, remote)
            elif args.pull:
                pull(cls, data_dir, sql_file, remote)
            elif args.push:
                push(cls, data_dir, sql_file, remote)
            elif args.post_checkout:
                checkout(cls, data_dir, sql_file, remote)

        return cls
    return decorator
