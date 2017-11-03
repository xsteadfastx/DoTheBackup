import logging
from unittest.mock import patch

import pytest
import yaml
from click.testing import CliRunner

from dothebackup import ui


@pytest.mark.parametrize('config,args,expected_log_level,expected_cmds', [
    (
        {
            'logs': {
                'keep': 1
            },
            'backup': {
                'testing': {
                    'enabled': True,
                    'type': 'rsync',
                    'mode': 'once',
                    'source': '/foo/bar',
                    'destination': '/backup/foo'
                }
            }
        },
        None,
        logging.WARNING,
        {
            'testing': [
                ['rsync', '-av', '--delete', '/foo/bar/', '/backup/foo']
            ]
        }
    ),
    (
        {
            'logs': {
                'keep': 1
            },
            'backup': {
                'testing': {
                    'enabled': True,
                    'type': 'rsync',
                    'mode': 'once',
                    'source': '/foo/bar',
                    'destination': '/backup/foo'
                }
            }
        },
        ['--debug', 'info'],
        logging.INFO,
        {
            'testing': [
                ['rsync', '-av', '--delete', '/foo/bar/', '/backup/foo']
            ]
        }
    ),
    (
        {
            'logs': {
                'keep': 1
            },
            'backup': {
                'testing': {
                    'enabled': True,
                    'type': 'rsync',
                    'mode': 'once',
                    'source': '/foo/bar',
                    'destination': '/backup/foo'
                }
            }
        },
        ['--debug', 'debug'],
        logging.DEBUG,
        {
            'testing': [
                ['rsync', '-av', '--delete', '/foo/bar/', '/backup/foo']
            ]
        }
    ),
])
@patch('dothebackup.runner.run_commands')
def test_main(
        mock_run_commands,
        config,
        args,
        expected_log_level,
        expected_cmds,
        tmpdir
):
    # add logdir
    config['logs']['dir'] = tmpdir.mkdir('logs').strpath

    # write config
    config_file = tmpdir.join('config.yaml')
    config_file.write(
        yaml.dump(config, default_flow_style=False)
    )

    runner = CliRunner()
    extras_list = [config_file.strpath]
    if args:
        extras_list = args + extras_list
    print(extras_list)
    result = runner.invoke(ui.main, extras_list)

    assert result.exit_code == 0
    assert mock_run_commands.call_count == 1

    with open(config_file.strpath, 'r') as f:
        loaded_conf = yaml.load(f)
        log_dir = loaded_conf['logs']['dir']
        log_keep = loaded_conf['logs']['keep']

    mock_run_commands.assert_called_with(
        expected_cmds,
        log_dir=log_dir,
        log_keep=log_keep,
        test=False
    )

    assert logging.getLogger().getEffectiveLevel() == expected_log_level
