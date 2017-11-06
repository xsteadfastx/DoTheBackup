"""Utils."""

import logging
import os
import subprocess
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator, List

from dothebackup.constants import PIDFILE

LOG = logging.getLogger(__name__)


def absolutenormpath(path: str) -> str:
    """Returns a absolute normalized path.

    :param path: Path
    :returns: Absolute path
    """
    abspath = os.path.abspath(os.path.normpath(path))
    LOG.debug('absolute path: %s', abspath)

    return abspath


def today() -> str:
    """Returns todays day string.

    :returns: Today day string
    """
    return datetime.utcnow().strftime('%d')


def git_cloned_yet(path: str) -> bool:
    """Returns if path contains a git repository.

    :param path: A path
    :returns: If path contains a git repositoy
    """
    is_dir = os.path.isdir(os.path.join(path, '.git'))
    LOG.debug('git cloned yes: %s', is_dir)

    return is_dir


def git_something_to_commit(path: str) -> bool:
    """Returns if path has something to commit.

    :param path: A path
    :returns: If path has something to commit
    """
    command = ['cd', path, '&&', 'git', 'status', '--porcelain']
    stdout = subprocess.check_output(' '.join(command), shell=True)

    something_to_commit = bool(stdout)

    LOG.debug('something to commit: %s', something_to_commit)

    return something_to_commit


def return_code(exitcodes: List[int]) -> int:
    """Get overalls exitcode out of a list of exitcodes.

    :param exitcodes: List of exitcodes
    :returns: Return exit code 1 if something different than 0 is in the list
    """
    code = 0
    for exitcode in exitcodes:
        if exitcode != 0:
            code = 1

    return code


@contextmanager
def pidfile() -> Iterator[None]:
    """Contextmanager to create a Pidfile for the
    DoTheBackup process and removes it afterwards.
    """
    pid = Path(PIDFILE)
    try:
        with pid.open(mode='w') as pid_file:
            pid_file.write(str(os.getpid()))
        yield
    finally:
        pid.unlink()
