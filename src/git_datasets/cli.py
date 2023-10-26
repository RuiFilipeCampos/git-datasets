""" Command-line argument parser for git hooks and operations. """

import argparse
from typing import Protocol

class ParserArgsProtocol(Protocol):
    """ Return values of `parse_args` """

    pre_commit: bool
    pull: bool
    push: bool
    post_checkout: bool

def parse_args() -> ParserArgsProtocol:
    """
    Parses command-line arguments to determine the specified git action.
    """
    parser = argparse.ArgumentParser()
    actions = [ "--pre-commit", "--pull", "--push", "--post-checkout"]
    group = parser.add_mutually_exclusive_group()
    for action in actions:
        group.add_argument(action, action="store_true")
    return parser.parse_args()
