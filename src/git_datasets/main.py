"""
Entrypoint for the git-datasets package.
"""

import logging
import sys

import os
import os.path


from git_datasets.cli import parse_args
from git_datasets.config import DatasetRunConfig
from git_datasets.types import DecoratedClass, Decorator

from git_datasets.git_hooks.pre_commit import pre_commit
from git_datasets.git_hooks.pull import pull
from git_datasets.git_hooks.push import push
from git_datasets.git_hooks.checkout import checkout


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("git_datasets")

def dataset(cls: DecoratedClass) -> DecoratedClass:

    args = parse_args()
    config = DatasetRunConfig()

    if args.pre_commit:
        pre_commit(cls, config)
    elif args.pull:
        pull(cls, config)
    elif args.push:
        push(cls, config)
    elif args.post_checkout:
        checkout(cls, config)
    else:
        raise NotImplementedError("Read mode not implemented.")

    return cls

