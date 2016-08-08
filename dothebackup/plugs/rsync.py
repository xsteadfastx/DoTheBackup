import arrow
import logging
import os

from dothebackup import plugins


log = logging.getLogger(__name__)


def normalize_path(path):
    """Returns a normalized path.

    Rsync needs a normalized path and special handing if its a ssh path.

    :param path: Path to normalize
    :type path: str
    :returns: Normalized path
    :rtype: str
    """
    if '@' in path:
        split_path = path.split(':')
        split_path[1] = os.path.normpath(split_path[1])

        return ':'.join(split_path)

    else:
        return os.path.normpath(path)


@plugins.required_executables(['rsync'])
@plugins.required_keys(['source', 'destination', 'mode'])
def main(config):
    """Command builder.

    :param config: config snippet for this plugin
    :type config: dict
    :returns: Commands to create the backup
    :rtype: list
    """
    # create time variables
    now = arrow.utcnow()
    today_day_of_month = now.format('DD')
    yesterday_day_of_month = now.replace(days=-1).format('DD')
    today_day_of_week = now.format('d')
    yesterday_day_of_week = now.replace(days=-1).format('d')

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
