""" TODO: docstring """

from git_datasets.types import DecoratedClass
from git_datasets.config import DatasetRunConfig
from git_datasets.logging import get_logger

logger = get_logger(__name__)

def pull(cls: DecoratedClass, config: DatasetRunConfig):
    """ Pull data from remote. """

    logger.error("Pull not implemented.")
    raise SystemExit