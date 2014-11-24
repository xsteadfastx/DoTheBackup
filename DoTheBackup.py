'''
Usage:
    DoTheBackup.py (-f <config> | --file <config>) [--verbose]
    DoTheBackup.py -h | --help

Options:
    -h --help        Show this screen.
    -f --file        Reads config from YAML File.
    -v --verbose     Prints the created commands used.
'''
import arrow
import yaml
import os
import subprocess
from docopt import docopt


NOW = arrow.utcnow()
TODAY = NOW.format('DD')
YESTERDAY = NOW.replace(days=-1).format('DD')


class CreateCmds(object):
    def __init__(self, config):
        self.config = config
        # list commands
        self.cmds = []

    def cmd_list(self):
        ''' returns list of commands '''
        # rsync
        if self.config['type'] == 'rsync_month' or \
           self.config['type'] == 'rsync_once':
            self._rsync_month_once()
            return self.cmds

        # git mysql
        elif self.config['type'] == 'git_mysql':
            self._git_mysql()
            return self.cmds

    def _create_git_cmds(self):
        # adds db dump to git
        self.cmds.append(['cd {} &&'.format(self.config['destination']),
                          'git',
                          'add',
                          '{}.sql'.format(self.config['db_name'])])

        # commit changes
        self.cmds.append(['cd {} &&'.format(self.config['destination']),
                          'git',
                          'commit',
                          '-m',
                          '"daily backup"'])

        # if remote_name then create also a push command
        if self.config['remote_name']:
            self.cmds.append(['cd {} &&'.format(self.config['destination']),
                              'git',
                              'push',
                              self.config['remote_name'],
                              'master'])

    def _rsync_month_once(self):
        source = os.path.normpath(self.config['source']) + '/'
        destination = os.path.normpath(self.config['destination'])

        # adding basic rsync stuff
        cmd = ['rsync', '-av', '--delete']

        # check for exclude and include and add it to the rsync cmd list
        if 'exclude' in self.config:
            for sequence in self.config['exclude']:
                cmd.append('--exclude={}'.format(sequence))
        if 'include' in self.config:
            for sequence in self.config['include']:
                cmd.append('--include={}'.format(sequence))

        # do magic of type is month
        if self.config['type'] == 'rsync_month':
            # if using days you have to specify link-dest
            cmd.append('--link-dest=../{}'.format(YESTERDAY))
            destination = os.path.join(destination, TODAY)
        elif self.config['type'] == 'rsync_once':
            pass

        # adding source and destination to the rsync cmd list
        cmd.append(source)
        cmd.append(destination)

        # returns complete cmd list
        self.cmds.append(cmd)

    def _git_mysql(self):
        user = self.config['user']
        password = self.config['password']
        db_name = self.config['db_name']
        destination = os.path.normpath(self.config['destination'])
        output_file = os.path.join(
            destination, '{}.sql'.format(db_name))

        # add mysqldump stuff
        self.cmds.append(['mysqldump',
                          '-u{}'.format(user),
                          '-p{}'.format(password),
                          '--skip-extended-insert',
                          db_name,
                          '>',
                          output_file])

        self._create_git_cmds()


def from_file(arguments):
    # reading config from file
    with open(arguments['<config>'], 'r') as f:
        config = yaml.load(f)

    # work through config file
    for scalar, sequence in config['backup'].items():
        # check if enabled
        if sequence['enabled']:
            # create list for returncodes
            returncodes = []

            cmds_object = CreateCmds(sequence)
            cmd_list = cmds_object.cmd_list()

            # run through cmds
            first_cmd = True
            for cmd in cmd_list:
                cmd = ' '.join(cmd)

                # define mode to open file. its different on the first run
                if first_cmd:
                    open_mode = 'w'
                    first_cmd = False
                else:
                    open_mode = 'a'

                # create process
                if arguments['--verbose']:
                    print(cmd)

                proc = subprocess.Popen(cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        shell=True)

                # get abspath of log_dir
                log_dir = os.path.abspath(os.path.normpath(config['log_dir']))

                # write logfile
                with open(
                    os.path.join(log_dir,
                                 '{}.log'.format(scalar)), open_mode) as f:
                    for line in proc.stdout:
                        f.write(line.decode('utf-8'))
                    proc.wait()

                # store returncode
                returncodes.append(proc.returncode)

            # write exit code
            code = 0
            for exitcode in returncodes:
                if exitcode != 0:
                    code = 1

            with open(
                os.path.join(log_dir,
                             '{}.log'.format(scalar)), 'a') as f:
                f.write('Exit Code: {}'.format(code))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['--file']:
        from_file(arguments)
