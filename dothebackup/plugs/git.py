import logging

from dothebackup import plugins, utils
from dothebackup.types import CommandListType, ConfigType


log = logging.getLogger(__name__)


@plugins.required_executables(['git'])
@plugins.required_keys(['source', 'destination'])
def main(config: ConfigType) -> CommandListType:
    """Command builder.

    :param config: config snippet for this plugin
    :returns: Commands to create the backup
    """
    commands = []

    # if there is no cloned repo yet... do it first
    if not utils.git_cloned_yet(config['destination']):
        commands.append(['git', 'clone', config['source'],
                         config['destination']])

    commands.append(['cd', config['destination'], '&&', 'git', 'pull'])

    return commands
