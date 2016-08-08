import logging
import os
import subprocess

from datetime import datetime


log = logging.getLogger(__name__)


def absolutenormpath(path):
    """Returns a absolute normalized path.

    :param path: Path
    :type path: str
    :returns: Absolute path
    :rtype: str
    """
    abspath = os.path.abspath(os.path.normpath(path))
    log.debug('absolute path: {}'.format(abspath))

    return abspath


def today():
    """Returns todays day string.

    :returns: Today day string
    :rtype: str
    """
    return datetime.utcnow().strftime('%d')


def git_cloned_yet(path):
    """Returns if path contains a git repository.

    :param path: A path
    :type path: str
    :returns: If path contains a git repositoy
    :rtype: bool
    """
    is_dir = os.path.isdir(os.path.join(path, '.git'))
    log.debug('git cloned yes: {}'.format(is_dir))

    return is_dir


def git_something_to_commit(path):
    """Returns if path has something to commit.

    :param path: A path
    :type path: str
    :returns: If path has something to commit
    :rtype: bool
    """
    command = ['cd', path, '&&', 'git', 'status', '--porcelain']
    stdout = subprocess.check_output(' '.join(command), shell=True)

    if stdout:
        something_to_commit = True
    else:
        something_to_commit = False

    log.debug('something to commit: {}'.format(something_to_commit))

    return something_to_commit
