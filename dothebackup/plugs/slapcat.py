from os.path import join

from dothebackup import plugins, tools


@plugins.required_executables(['slapcat'])
@plugins.required_keys(['destination', 'mode'])
def main(config):
    commands = []

    destination = config['destination']

    # git init if its not a repo yet
    if config['mode'] == 'git':
        cloned_yet = tools.git_cloned_yet(destination)
        if not cloned_yet:
            commands.append(['cd', destination, '&&', 'git', 'init'])

    # slapcat command
    commands.append(['slapcat', '-l',
                     join(tools.absolutenormpath(destination), 'backup.ldif')])

    # commit if git mode is used
    if config['mode'] == 'git':
        if not cloned_yet or tools.git_something_to_commit(destination):
            commands.append(
                ['cd', destination,
                 '&&',
                 'git', 'add', 'backup.ldif',
                 '&&',
                 'git', 'commit', '-m', '"new export"'])

    return commands
