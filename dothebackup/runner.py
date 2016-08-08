from __future__ import print_function
import datetime
import logging
import os
import subprocess
import sys
import yaml

from dothebackup import tools
from dothebackup.plugins import load_plugins


log = logging.getLogger(__name__)


def parse_config(configfile):
    '''Read config file.
    '''
    return yaml.load(configfile)


def check_config_keys(config, key_list):
    '''Aborts if keys are not set in config.
    '''
    for key in key_list:
        if key not in config.keys():
            print('ERROR: "{}" is missing in the config.'.format(key))
            sys.exit()


def check_plugin(name):
    '''Aborts and throw an error if plugin is not there as defined as type
    in config.
    '''
    if name not in sys.modules.keys():
        print('ERROR: Plugin "{}" could not be found.'.format(name))
        sys.exit()


def builder(config, name):
    '''Builds a dict of commands.
    '''
    commands = {}
    today = tools.today()
    plugins = load_plugins()

    for scalar, sequence in config['backup'].items():

        # if there is a name it will ignore the 'enabled' key
        if not name:

            if 'enabled' not in sequence.keys():
                print('ERROR: "enabled" is missing in the config.')
                sys.exit()

            if not sequence['enabled']:
                log.info('skipping {}'.format(scalar))
                continue

            # if days are in config and its not a days defined it will continue
            # the for loop
            if 'days' in sequence.keys():
                if today not in sequence['days']:
                    log.info('skipping {}'.format(scalar))
                    continue

        # if there is a name defined and its not the name of the scalar
        # it will continue the for loop
        if name and name != scalar:
            continue

        # check if plugin can be found
        check_plugin(sequence['type'])

        # add plugin commands to command dict
        commands[scalar] = plugins[sequence['type']](sequence)

    if name and not commands:
        print('ERROR: "{}" could not be found in config.'.format(name))
        sys.exit()

    return commands


def print_commands(commands):
    '''Prints the commands that would be used.
    '''
    for item in commands.items():
        print(item[0])
        for character in item[0]:
            print('-', end='')
        print('\n')
        for command in item[1]:
            print('  * {}'.format(' '.join(command)))
        print('\n')


def run_commands(commands, test, log_dir):
    '''Running the commands.
    '''
    # in test mode it will print all the commands it would run for
    # each item in the config
    if test:
        print_commands(commands)

    else:
        # normalize log_dir and create it if its not existing
        log_dir = os.path.abspath(os.path.normpath(log_dir))
        log.debug('logdir: {}'.format(log_dir))

        if not os.path.exists(log_dir):
            log.debug('create: {}'.format(log_dir))
            os.makedirs(log_dir)

        for item in commands.items():
            log.debug('item: {}'.format(item))
            name, command_list = item

            # collects the return codes of all sub commands
            return_codes = []

            # define logfile
            logfile = os.path.join(log_dir, '{}.log'.format(name))
            log.debug('logfile: {}'.format(logfile))

            # run through commands
            first_cmd = True
            starting_time = datetime.datetime.now()
            for command in command_list:

                # define mode to open file. its different on the first run
                if first_cmd:
                    open_mode = 'w'
                    first_cmd = False
                else:
                    open_mode = 'a'

                # create process
                command = ' '.join(command)
                log.debug('command: {}'.format(command))

                log.debug('start subprocess')
                proc = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True
                )
                log.debug('stop subprocess')

                # write logfile
                log.debug('write log: {}'.format(logfile))
                with open(logfile, open_mode) as f:
                    for line in proc.stdout:
                        f.write(line.decode('utf-8'))

                    proc.wait()
                log.debug('done writing logfile')

                # store returncode
                returncode = proc.returncode
                log.debug('returncode: {}'.format(returncode))
                return_codes.append(returncode)

            # write exit code
            code = 0
            for exitcode in return_codes:
                if exitcode != 0:
                    code = 1
            log.debug('exitcode: {}'.format(code))

            log.debug('write metadata')
            with open(logfile, 'a') as f:
                finishing_time = datetime.datetime.now()
                f.write('Finished at: {}\n'.format(
                    finishing_time.strftime("%Y-%m-%d %H:%M"))
                )
                f.write(
                    'Total runtime: {} seconds.\n'.format(
                        (finishing_time - starting_time).total_seconds())
                )
                f.write('Exit code: {}\n'.format(code))
            log.debug('done')


def get_started(configfile, name, test):
    # read config
    config = parse_config(configfile)

    # if backup and log_dir is not in config it will abort
    check_config_keys(config, ['backup', 'log_dir'])

    # get everything started
    commands = builder(config, name=name)
    run_commands(commands, test=test, log_dir=config['log_dir'])
