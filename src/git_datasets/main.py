"""
main.py - Entrypoint for the git-datasets package.
"""

from git_datasets.logging import get_logger
from git_datasets.cli import parse_args
from git_datasets.hooks import GitHooks
from git_datasets.types import DecoratedClass
from git_datasets.parquet_vm import LocalParquetVM

logger = get_logger(__name__)

def dataset(cls: DecoratedClass) -> DecoratedClass:
    """ Register an annotated class as a dataset.  """

    parquet_vm = LocalParquetVM()
    hooks = GitHooks(cls, parquet_vm)
    cli_args = parse_args()

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
