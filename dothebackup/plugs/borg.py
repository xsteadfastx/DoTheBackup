import logging

from dothebackup import plugins
from dothebackup.types import CommandListType, ConfigType

import pendulum


log = logging.getLogger(__name__)


@plugins.required_executables(['borg'])
@plugins.required_keys(['source', 'destination'])
def main(config: ConfigType) -> CommandListType:
    """Command builder.

    :param config: config snippt for this plugin
    :returns: Commands to create the backup
    """
    commands = []  # type: List[List[str]]

    # create backup
    commands.append(
        [
            'BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes',
            'borg', 'create', '-v', '--stats',
            '{}::{}'.format(
                config['destination'],
                pendulum.now().format('%Y-%m-%d-%H-%M')
            )
        ]
    )

    # adding sources
    commands[-1].extend(config['source'])

    # add excludes
    if 'exclude' in config.keys():
        for exclude in config['exclude']:
            commands[-1].append('--exclude {}'.format(exclude))

    # prune
    if 'keep' in config.keys():
        prune_command = [
            'borg', 'prune', '-v', '--list',
            config['destination']
        ]  # type: List[str]

        if 'daily' in config['keep'].keys():
            prune_command.append(
                '--keep-daily={}'.format(config['keep']['daily'])
            )

        if 'weekly' in config['keep'].keys():
            prune_command.append(
                '--keep-weekly={}'.format(config['keep']['weekly'])
            )

        if 'monthly' in config['keep'].keys():
            prune_command.append(
                '--keep-monthly={}'.format(config['keep']['monthly'])
            )

        commands.append(prune_command)

    # check
    if 'check' in config.keys() and config['check']:
        commands.append(['borg', 'check', config['destination']])

    return commands
