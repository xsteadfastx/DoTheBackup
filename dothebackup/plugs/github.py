import os
import requests

from dothebackup import plugins


def get_repos(username):
    r = requests.get('https://api.github.com/users/{}/repos'.format(username))

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
        if not os.path.isdir(os.path.join(destination, '.git')):
            commands.append(['git', 'clone', repo['clone_url'], destination])

        # add git pull command
        commands.append(['cd', destination, '&&', 'git', 'pull'])

    return commands
