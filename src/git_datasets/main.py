""" Entrypoint for the git-datasets package. """

from git_datasets.logging import get_logger
from git_datasets.types import DecoratedClass

logger = get_logger(__name__)


def dataset(cls: DecoratedClass) -> DecoratedClass:
    """ Register an annotated class as a dataset.

    TODO:
        config = read_repo_config()
        should read from config file in hiddne folder

    """

    # pylint: disable=import-outside-toplevel
    # reason: delaying imports until needed

    from git_datasets.virtual_memory import LocalCheckpoinstVM

    virtual_memory = LocalCheckpoinstVM()

    from git_datasets.hooks import GitHooks

    hooks = GitHooks(cls, virtual_memory)

    from git_datasets.cli import parse_args

    cli_args = parse_args()

    if cli_args.pre_commit:
        hooks.pre_commit()
    elif cli_args.post_commit:
        hooks.post_commit()
    elif cli_args.post_checkout:
        hooks.post_checkout()
    elif cli_args.pull:
        hooks.pull()
    elif cli_args.push:
        hooks.push()
    else:
        logger.info("Initiating dry-run.")
        logger.error("Read mode not implemented.")
        raise SystemExit

    return cls

 