"""TODO: Docstring"""

from git_datasets.types import DecoratedClass
from git_datasets.config import DatasetRunConfig
from git_datasets.logging import get_logger

logger = get_logger(__name__)

def checkout(cls: DecoratedClass, config: DatasetRunConfig):
    """ Checkout the dataset. """

    logger.error("Checkout not implemented.")
    raise SystemExit
