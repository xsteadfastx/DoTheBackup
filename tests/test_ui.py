from unittest.mock import patch

from click.testing import CliRunner

from dothebackup import ui

import yaml


@patch('dothebackup.runner.run_commands')
def test_main(mock_run_commands, config):
    runner = CliRunner()
    result = runner.invoke(ui.main, [config])

    assert result.exit_code == 0
    assert mock_run_commands.call_count == 1

    with open(config, 'r') as f:
        log_dir = yaml.load(f)['logs']['dir']

    mock_run_commands.assert_called_with(
        {
            'testing': [
                ['rsync', '-av', '--delete', '/foo/bar/', '/backup/foo']
            ]
        },
        log_dir=log_dir,
        log_keep=1,
        test=False
    )
