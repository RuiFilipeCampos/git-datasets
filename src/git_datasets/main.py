"""
main.py - Entrypoint for the git-datasets package.
"""

from git_datasets.cli import parse_args
from git_datasets.config import DatasetRunConfig
from git_datasets.logging import get_logger
from git_datasets.types import DecoratedClass

from git_datasets.git_hooks import pre_commit, pull, push, checkout

logger = get_logger(__name__)

def dataset(cls: DecoratedClass) -> DecoratedClass:
    """ Register an annotated class as a dataset.  """

    args = parse_args()

    init_args = {
        "dataset_name": cls.__name__.lower(),
    }

    with DatasetRunConfig.init(**init_args) as config:
        if args.pre_commit:
            pre_commit(cls, config)
        elif args.pull:
            pull(cls, config)
        elif args.push:
            push(cls, config)
        elif args.post_checkout:
            checkout(cls, config)
        else:
            logger.error("Read mode not implemented.")
            raise SystemExit

    return cls
