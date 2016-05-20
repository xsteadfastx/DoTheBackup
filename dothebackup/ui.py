import click

from dothebackup.runner import get_started


@click.command()
@click.argument('configfile', type=click.File('r'))
@click.option('--name',
              help='Run a specific job from the config.')
@click.option('--test', is_flag=True,
              help='Only prints the created commands that would be used.')
@click.version_option()
def main(configfile, name, test):
    '''Commandline interface.
    '''
    get_started(configfile, name=name, test=test)
