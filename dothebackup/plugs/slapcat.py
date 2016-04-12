from os.path import join

from dothebackup import plugins, tools


@plugins.required_executables(['slapcat'])
@plugins.required_keys(['destination', 'mode'])
def main(config):
    commands = []

    # git init if its not a repo yet
    if config['mode'] == 'git':
        if not tools.git_cloned_yet(config['destination']):
            commands.append(['cd', config['destination'], '&&',
                             'git', 'init'])

    # slapcat command
    commands.append(['slapcat', '-l',
                     join(tools.absolutenormpath(config['destination']),
                          'backup.ldif')])

    # commit if git mode is used
    if config['mode'] == 'git':
        if tools.git_something_to_commit(config['destination']):
            commands.append(
                ['cd', config['destination'],
                 '&&',
                 'git', 'add', 'backup.ldif',
                 '&&',
                 'git', 'commit', '-m', '"new export"'])

    return commands
