from datetime import datetime
import os
import subprocess


def absolutenormpath(path):
    '''Returns a absolute normalized path.
    '''
    return os.path.abspath(os.path.normpath(path))


def today():
    '''Returns todays day string.
    '''
    return datetime.utcnow().strftime('%d')


def git_cloned_yet(path):
    '''Returns if path contains a git repository.
    '''
    return os.path.isdir(os.path.join(path, '.git'))


def git_something_to_commit(path):
    '''Returns if path has something to commit.
    '''
    command = ['cd', path, '&&', 'git', 'status', '--porcelain']
    stdout = subprocess.check_output(' '.join(command), shell=True)

    if stdout:
        return True
    else:
        return False
