import click
import logging

from dothebackup.runner import get_started


@click.command()
@click.argument('configfile', type=click.File('r'))
@click.option('--name',
              help='Run a specific job from the config.')
@click.option('--test', is_flag=True,
              help='Only prints the created commands that would be used.')
@click.option('--debug', is_flag=True,
              help='Debugging messages.')
@click.version_option()
def main(configfile, name, test, debug):
    '''Commandline interface.
    '''
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    get_started(configfile, name=name, test=test)
