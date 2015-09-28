from __future__ import print_function
import click
import os
import subprocess
import sys
import yaml

from dothebackup import PLUGINS


def parse_config(configfile):
    '''Read config file.
    '''
    with open(configfile, 'r') as f:
        config = yaml.load(f)

    return config


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


def builder(config):
    '''Builds a dict of commands.
    '''
    commands = {}

    for scalar, sequence in config['backup'].items():
        if 'enabled' not in sequence.keys():
            print('ERROR: "enabled" is missing in the config.')
            sys.exit()

        if not sequence['enabled']:
            print('skipping {}'.format(scalar))
            continue

        # check if plugin can be found
        check_plugin(sequence['type'])

        # add plugin commands to command dict
        commands[scalar] = PLUGINS[sequence['type']](sequence)

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


def runner(commands, test, log_dir):
    '''Running the commands.
    '''
    # in test mode it will print all the commands it would run for
    # each item in the config
    if test:
        print_commands(commands)

    else:
        # normalize log_dir and create it if its not existing
        log_dir = os.path.abspath(os.path.normpath(log_dir))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        for item in commands.items():
            name, command_list = item

            # collects the return codes of all sub commands
            return_codes = []

            # define logfile
            log = os.path.join(log_dir, '{}.log'.format(name))

            # run through commands
            first_cmd = True
            for command in command_list:

                # define mode to open file. its different on the first run
                if first_cmd:
                    open_mode = 'w'
                    first_cmd = False
                else:
                    open_mode = 'a'

                # create process
                command = ' '.join(command)
                proc = subprocess.Popen(command,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        shell=True)

                # write logfile
                with open(log, open_mode) as f:
                    for line in proc.stdout:
                        f.write(line.decode('utf-8'))

                    proc.wait()

                # store returncode
                return_codes.append(proc.returncode)

            # write exit code
            code = 0
            for exitcode in return_codes:
                if exitcode != 0:
                    code = 1

            with open(log, 'a') as f:
                f.write('Exit code: {}'.format(code))


def get_started(configfile, test):
    # read config
    config = parse_config(configfile)

    # if backup and log_dir is not in config it will abort
    check_config_keys(config, ['backup', 'log_dir'])

    # get everything started
    commands = builder(config)
    runner(commands, test, config['log_dir'])


@click.command()
@click.argument('configfile', required=True)
@click.option('--test', is_flag=True,
              help='Only prints the created commands that would be used.')
@click.version_option()
def main(configfile, test):
    '''Commandline interface.
    '''
    get_started(configfile, test)
