import os
import requests
import logging

from dothebackup import plugins, utils


log = logging.getLogger(__name__)


def get_repos(username):
    r = requests.get('https://api.github.com/users/{}/repos'.format(username))

    log.info('got repos from github api')

    # a nice python dict
    return r.json()


@plugins.required_executables(['git'])
@plugins.required_keys(['username', 'destination'])
def main(config):
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
