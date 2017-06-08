import logging

from os import path

from dothebackup import plugins, utils
from dothebackup.types import CommandListType, ConfigType


log = logging.getLogger(__name__)


@plugins.required_executables(['mysqldump', 'git'])
@plugins.required_keys(
    [
        'mode',
        'server',
        'username',
        'password',
        'database',
        'destination'
    ]
)
def main(config: ConfigType) -> CommandListType:
    """Command builder.

    :param config: config snippet for this plugin
    :returns: Commands to create the backup
    """
    commands = []

    destination = config['destination']

    # if commiting every dump to a git repo it has to init first if
    # its not there
    if config['mode'] == 'git':
        cloned_yet = utils.git_cloned_yet(destination)
        if not cloned_yet:
            commands.append(['cd', destination, '&&', 'git', 'init'])

    # mysqldump command
    commands.append(
        [
            'mysqldump', '--skip-extended-insert', '--skip-comments',
            '--user={}'.format(config['username']),
            '--password={}'.format(config['password']),
            '--host={}'.format(config['server']),
            config['database'],
            '>',
            path.join(
                utils.absolutenormpath(destination),
                '{}.sql'.format(config['database'])
            )
        ]
    )

    # commit if git mode is used
    if config['mode'] == 'git':

        # only commit if there is something to be commited
        if not cloned_yet or utils.git_something_to_commit(destination):

            commands.append(
                [
                    'cd', destination,
                    '&&',
                    'git', 'add', '{}.sql'.format(config['database']),
                    '&&',
                    'git', 'commit', '-m', '"new dump"'
                ]
            )

    return commands
