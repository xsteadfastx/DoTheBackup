import logging

import os

from dothebackup import plugins
from dothebackup.types import CommandListType, ConfigType

import pendulum


log = logging.getLogger(__name__)


def normalize_path(path: str) -> str:
    """Returns a normalized path.

    Rsync needs a normalized path and special handing if its a ssh path.

    :param path: Path to normalize
    :returns: Normalized path
    """
    if '@' in path:
        split_path = path.split(':')
        split_path[1] = os.path.normpath(split_path[1])

        return ':'.join(split_path)

    else:
        return os.path.normpath(path)


@plugins.required_executables(['rsync'])
@plugins.required_keys(['source', 'destination', 'mode'])
def main(config: ConfigType) -> CommandListType:
    """Command builder.

    :param config: config snippet for this plugin
    :returns: Commands to create the backup
    """
    # create time variables
    now = pendulum.utcnow()

    today_day_of_month = now.format('%d')
    yesterday_day_of_month = now.yesterday().format('%d')

    today_day_of_week = now.format('%w')
    yesterday_day_of_week = now.yesterday().format('%w')

    # adding basic rsync stuff
    command = ['rsync', '-av', '--delete']

    # generate paths
    source = normalize_path(config['source']) + '/'
    destination = normalize_path(config['destination'])

    # add ssh as shell if its needed
    if '@' in destination:
        command.append('-e ssh')

    # check for exclude and include and add it to the rsync command list
    if 'exclude' in config.keys():
        for item in config['exclude']:
            command.append('--exclude={}'.format(item))

    if 'include' in config.keys():
        for item in config['include']:
            command.append('--include={}'.format(item))

    # handling rsync mode
    if config['mode'] == 'month':
        # if using days you have to specify link-dest
        command.append('--link-dest=../{}'.format(yesterday_day_of_month))
        destination = os.path.join(destination, today_day_of_month)

    elif config['mode'] == 'week':
        # if using days you have to specify link-dest
        command.append('--link-dest=../{}'.format(yesterday_day_of_week))
        destination = os.path.join(destination, today_day_of_week)

    elif config['mode'] == 'once':
        # once mode doesnt need another commands
        pass

    # append source and destination
    command.append(source)
    command.append(destination)

    return [command]
