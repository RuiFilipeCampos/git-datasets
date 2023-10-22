""" 
commands.py - interactions with the command line
"""

import subprocess

def get_git_root_path() -> str | None:
    """ Retrieve the root path of the current Git repository. """

    try:
        commands = ['git', 'rev-parse', '--show-toplevel']
        base_path = subprocess               \
                    .check_output(commands)  \
                    .strip()                 \
                    .decode('utf-8')

        return base_path
    except subprocess.CalledProcessError:
        return None
