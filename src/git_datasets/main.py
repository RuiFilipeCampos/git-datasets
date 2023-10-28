"""
main.py - Entrypoint for the git-datasets package.
"""

from git_datasets.logging import get_logger
from git_datasets.cli import parse_args
from git_datasets.hooks import GitHooks
from git_datasets.types import DecoratedClass

logger = get_logger(__name__)

def dataset(cls: DecoratedClass) -> DecoratedClass:
    """ Register an annotated class as a dataset.  """

    cli_args = parse_args()

    parquet = ...
    hooks = GitHooks(cls, parquet)

    if cli_args.pre_commit:
        hooks.pre_commit()
    elif cli_args.post_commit:
        hooks.post_commit()
    elif cli_args.pull:
        hooks.pull()
    elif cli_args.push:
        hooks.push()
    else:
        logger.info("Initiating dry-run.")
        logger.error("Read mode not implemented.")
        raise SystemExit

    return cls
