import logging

import os

from typing import Dict, List, Union

from dothebackup import plugins, utils
from dothebackup.types import CommandListType, ConfigType

import requests


log = logging.getLogger(__name__)


def get_repos(username: str) -> List[Dict[str, Union[int, str, Dict]]]:
    """Create a GET request on the github api to get all repos from a user.

    :param username: github username
    :returns: Full JSON dictionary of user repos from github
    """
    r = requests.get('https://api.github.com/users/{}/repos'.format(username))

    log.info('got repos from github api')

    # a nice python dict
    return r.json()


@plugins.required_executables(['git'])
@plugins.required_keys(['username', 'destination'])
def main(config: ConfigType) -> CommandListType:
    """Command builder.

    :param config: config snippet for this plugin
    :returns: Commands to create the backup
    """
    commands = []

    # walk through the github repos
    for repo in get_repos(config['username']):

        destination = os.path.join(config['destination'], repo['name'])

        # if the repo is not cloned yet, do it first
        if not utils.git_cloned_yet(destination):
            commands.append(['git', 'clone', repo['clone_url'], destination])

        # add git pull command
        commands.append(['cd', destination, '&&', 'git', 'pull'])

    return commands
