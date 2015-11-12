from os import path

from dothebackup import plugins, tools


@plugins.required_executables(['mysqldump', 'git'])
@plugins.required_keys(['mode', 'server', 'username', 'password', 'database',
                        'destination'])
def main(config):
    commands = []

    # if commiting every dump to a git repo it has to init first if
    # its not there
    if config['mode'] == 'git':
        if not tools.git_cloned_yet(config['destination']):
            commands.append(['cd', config['destination'], '&&',
                             'git', 'init'])

    # mysqldump command
    commands.append(['mysqldump', '--skip-extended-insert', '--skip-comments',
                     '--user={}'.format(config['username']),
                     '--password={}'.format(config['password']),
                     '--host={}'.format(config['server']),
                     config['database'],
                     '>',
                     path.join(
                         tools.absolutenormpath(config['destination']),
                         '{}.sql'.format(config['database']))])

    # commit if git mode is used
    if config['mode'] == 'git':

        # only commit if there is something to be commited
        if tools.git_something_to_commit(config['destination']):

            commands.append(['cd', config['destination'],
                             '&&',
                             'git', 'add', '{}.sql'.format(config['database']),
                             '&&',
                             'git', 'commit', '-m', '"new dump"'])

    return commands
