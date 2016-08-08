import logging
import os

from dothebackup import plugins
from dothebackup.utils import absolutenormpath


log = logging.getLogger(__name__)


@plugins.required_executables(['tar'])
@plugins.required_keys(['source', 'destination'])
def main(config):
    """Command builder.

    :param config: config snippet for this plugin
    :type config: dict
    :returns: Commands to create the backup
    :rtype: list
    """
    command = ['tar', '-vcp']

    # parse compress level out of destination filename
    extension = os.path.splitext(config['destination'])[1]

    if extension == '.bz2':
        command.append('-j')

    elif extension == '.gz':
        command.append('-z')

    elif extension == '.xz':
        command.append('-J')

    else:
        pass

    # add '-f' to command list for storing the tar in a file
    command.append('-f')

    # add destination
    command.append(absolutenormpath(config['destination']))

    # add dirs that get into the tarball
    for i in config['source']:
        command.append(absolutenormpath(i))

    return [command]
