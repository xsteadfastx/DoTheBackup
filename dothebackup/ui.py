import logging

from typing import IO

import click

from dothebackup.runner import get_started


@click.command()
@click.argument('configfile', type=click.File('r'))
@click.option(
    '--name', '-n', help='Run a specific job from the config.'
)
@click.option(
    '--test', '-t', is_flag=True,
    help='Only prints the created commands that would be used.'
)
@click.option(
    '--debug', type=click.Choice(['debug', 'info']),
    help='Debug or verbose messages.'
)
@click.version_option()
def main(configfile: IO, name: str, test: bool, debug: str) -> None:
    """Commandline interface.
    """
    if debug:

        if debug == 'debug':
            level = logging.DEBUG
        elif debug == 'info':
            level = logging.INFO

        logging.basicConfig(level=level)

    get_started(configfile, name=name, test=test)
