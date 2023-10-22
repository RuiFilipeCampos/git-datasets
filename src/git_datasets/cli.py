"""TODO"""

import argparse

def parse_args():
    """ TODO """
    parser = argparse.ArgumentParser()
    actions = [ "--pre-commit", "--pull", "--push", "--post-checkout" ]
    group = parser.add_mutually_exclusive_group()
    for action in actions:
        group.add_argument(action, action="store_true")
    return parser.parse_args()
