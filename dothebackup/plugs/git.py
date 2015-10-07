import os

from dothebackup import plugins


@plugins.required_executables(['git'])
@plugins.required_keys(['source', 'destination'])
def main(config):
    commands = []

    # if there is no cloned repo yet... do it first
    if not os.path.isdir(os.path.join(config['destination'], '.git')):
        commands.append(['git', 'clone', config['source'],
                         config['destination']])

    commands.append(['cd', config['destination'], '&&', 'git', 'pull'])

    return commands
