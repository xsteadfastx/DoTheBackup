'''
Usage:
    DoTheBackup.py (-f <config> | --file <config>)

Options:
    -f --file        Reads config from YAML File
'''
import arrow
import yaml
import os
import subprocess
from docopt import docopt


# gettings the arguments from docopt
ARGUMENTS = docopt(__doc__)

# define some times
NOW = arrow.utcnow()
TODAY = NOW.format('DD')
YESTERDAY = NOW.replace(days=-1).format('DD')


def rsync_cmd(config):
    source = os.path.normpath(config['source']) + '/'
    destination = os.path.normpath(config['destination'])

    # adding basic rsync stuff
    cmd = ['rsync', '-av', '--delete']

    # check for exclude and include and add it to the rsync cmd list
    if 'exclude' in config:
        for sequence in config['exclude']:
            cmd.append('--exclude={}'.format(sequence))
    if 'include' in config:
        for sequence in config['include']:
            cmd.append('--include={}'.format(sequence))

    # do magic of type is month
    if config['type'] == 'month':
        # for dealing with ssh source and destination:
        # the destination needs to be splitted to get the path
        cmd.append('--link-dest={}'.format(
            os.path.join(destination.split(':')[-1], YESTERDAY)))
        destination = os.path.join(destination, TODAY)
    elif config['type'] == 'once':
        pass

    # adding source and destination to the rsync cmd list
    cmd.append(source)
    cmd.append(destination)

    # returns complete cmd list
    return cmd


def from_file():
    # load config file
    with open(ARGUMENTS['<config>']) as f:
        config = yaml.load(f)

    # work through config file
    for scalar, sequence in config['backup'].viewitems():
        # create process
        proc = subprocess.Popen(rsync_cmd(sequence),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        # get abspath of log_dir
        log_dir = os.path.abspath(os.path.normpath(config['log_dir']))

        # create log_dir if not there
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # write logfile
        with open(os.path.join(log_dir, '{}.log'.format(scalar)), 'w') as f:
            for line in proc.stdout:
                f.write(line)
            proc.wait()
            f.write('Exit Code: {}'.format(str(proc.returncode)))


def main():
    if '--file' or '-f' in ARGUMENTS:
        from_file()


if __name__ == '__main__':
    main()
