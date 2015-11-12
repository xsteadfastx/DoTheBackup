from dothebackup import plugins, tools


@plugins.required_executables(['git'])
@plugins.required_keys(['source', 'destination'])
def main(config):
    commands = []

    # if there is no cloned repo yet... do it first
    if not tools.git_cloned_yet(config['destination']):
        commands.append(['git', 'clone', config['source'],
                         config['destination']])

    commands.append(['cd', config['destination'], '&&', 'git', 'pull'])

    return commands
