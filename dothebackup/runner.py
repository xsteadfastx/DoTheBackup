import datetime

import logging

import subprocess

import sys

from typing import Dict, IO, List, Optional

from dothebackup import utils
from dothebackup.logger import Logger
from dothebackup.plugins import load_plugins
from dothebackup.types import ConfigType
from dothebackup.utils import return_code

import yaml


log = logging.getLogger(__name__)


def parse_config(configfile: IO) -> Dict:
    """Read config file.

    :param configfile: YAML config file
    :type configfile: _io.TextIOWrapper
    :returns: loaded configfile
    :rtype: dict
    """
    return yaml.load(configfile)


def check_config_keys(config: ConfigType, key_list: List) -> None:
    """Aborts if keys are not set in config.

    :param config: Config
    :param key_list: List of used keys
    :type config: dict
    :type key_list: list
    """
    for key in key_list:
        if key not in config.keys():
            print('ERROR: "{}" is missing in the config.'.format(key))
            sys.exit(1)


def check_plugin(name: str) -> None:
    """Aborts and throw an error if plugin is not there as defined as type
    in config.

    :param name: Name of plugin that is defined in the config
    :type name: str
    """
    if name not in sys.modules.keys():
        print('ERROR: Plugin "{}" could not be found.'.format(name))
        sys.exit(1)


def builder(
        config: Dict[str, Dict[str, Dict]],
        name: Optional[str]
) -> Dict[str, List[List[str]]]:
    """Builds a dict of commands.

    :param config: YAML config
    :param name: Name of a specific job to run
    :returns: A dict with all commands needed commands
    """
    commands = {}
    today = utils.today()
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
        log.debug('added command: {}'.format(commands[scalar]))

    if name and not commands:
        print('ERROR: "{}" could not be found in config.'.format(name))
        sys.exit(1)

    return commands


def print_commands(commands: Dict[str, List[List[str]]]) -> None:
    """Prints the commands that would be used.

    :param commands: Command dictionary
    """
    for item in commands.items():
        print(item[0])
        for character in item[0]:
            print('-', end='')
        print('\n')
        for command in item[1]:
            print('  * {}'.format(' '.join(command)))
        print('\n')


def run_commands(
        commands: Dict[str, List[List[str]]],
        test: bool,
        log_dir: str,
        log_keep: int
) -> None:
    """Running the commands.

    The actual runner. It will take the commands dictionary and run it one
    after another. There is also a test key. With this enabled it will only
    print the commands it would run.

    :param commands: Commands dictionary
    :param test: If test the commands only will be printed
    :param log_dir: Dictionary for logfiles
    :param log_keep: How many logs to keep from one job
    """
    # in test mode it will print all the commands it would run for
    # each item in the config
    if test:
        print_commands(commands)

    else:
        # list to store all return codes of all sub commands
        all_return_codes = []  # type: List[int]

        for item in commands.items():
            log.debug('item: {}'.format(item))
            name, command_list = item

            log.info('started item {}'.format(name))

            # collects the return codes of all sub commands
            return_codes = []

            # define logger for stdout logging
            logger = Logger(
                utils.absolutenormpath(log_dir),
                name,
                log_keep
            )

            # be sure that there is the log dir
            logger.create_log_dir()

            # roate logfiles
            logger.rotate()

            # run through commands
            starting_time = datetime.datetime.now()
            for command_item in command_list:

                # create process
                command = ' '.join(command_item)
                log.debug('command: {}'.format(command))
                proc = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True
                )
                log.debug('run command')

                # write logfile
                log.debug('write to logfile')
                with logger.logfile() as logfile:
                    for line in proc.stdout:
                        dec_line = line.decode('utf-8', 'replace')
                        log.debug(dec_line)
                        logfile.write(dec_line)

                    proc.wait()

                log.debug('done writing logfile')
                log.debug('done with command')

                # store returncode
                returncode = proc.returncode
                log.debug('returncode: {}'.format(returncode))
                return_codes.append(returncode)

            # get exit code
            code = return_code(return_codes)

            # store it in the return code list for all sub commands
            all_return_codes.append(code)

            log.debug('exitcode: {}'.format(code))

            log.debug('write metadata')
            with logger.logfile() as logfile:

                finishing_time = datetime.datetime.now()
                logfile.write('Finished at: {}\n'.format(
                    finishing_time.strftime("%Y-%m-%d %H:%M"))
                )

                logfile.write(
                    'Total runtime: {} seconds.\n'.format(
                        (finishing_time - starting_time).total_seconds())
                )

                logfile.write('Exit code: {}\n'.format(code))

            log.debug('metadata done')

            log.info('done with item {}'.format(name))

        # get overall return code and exit with it
        sys.exit(return_code(all_return_codes))


def get_started(configfile: IO, name: str, test: bool) -> None:
    """The entrypoint for the UI.

    This is used to get everything started up. It will read the config,
    check the keys, build the command dictionary and run them.

    :param configfile: The config file
    :param name: A name of a specific job
    :param test: Switch for only printing the commands
    """
    log.info('dothebackup starting')

    # read config
    log.info('parse config')
    config = parse_config(configfile)

    # if backup and log_dir is not in config it will abort
    log.info('check config')
    check_config_keys(config, ['backup', 'logs'])
    check_config_keys(config['logs'], ['dir', 'keep'])

    # get everything started
    log.info('build commands')
    commands = builder(config, name=name)

    log.info('run commands')
    run_commands(
        commands,
        test=test,
        log_dir=config['logs']['dir'],
        log_keep=config['logs']['keep']
    )
    log.info('dothebackup done')
