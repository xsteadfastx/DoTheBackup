"""Git."""

import logging

from dothebackup import plugins, utils
from dothebackup.types import COMMANDLISTTYPE, CONFIGTYPE

LOG = logging.getLogger(__name__)


@plugins.required_executables(['git'])
@plugins.required_keys(['source', 'destination'])
def main(config: CONFIGTYPE) -> COMMANDLISTTYPE:
    """Command builder.

    :param config: config snippet for this plugin
    :returns: Commands to create the backup
    """
    commands = []

    # if there is no cloned repo yet... do it first
    if not utils.git_cloned_yet(config['destination']):
        commands.append(
            [
                'git', 'clone', config['source'],
                config['destination']
            ]
        )

    commands.append(['cd', config['destination'], '&&', 'git', 'pull'])

    return commands
