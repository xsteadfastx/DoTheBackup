# pylint: disable=missing-docstring, redefined-builtin, invalid-name
# pylint: disable=unused-argument, unused-variable

from unittest.mock import patch

import pytest

from dothebackup import runner


def test_check_config_keys_abort(capsys):
    config = {
        'backup': {
            'test': {
                'type': 'rsync',
                'mode': 'once',
                'source': '/foo/bar',
                'destination': '/zack/bumm'
            }
        }
    }

    with pytest.raises(SystemExit) as excinfo:
        runner.check_config_keys(config, ['log_dir', 'backup'])

    out, _ = capsys.readouterr()

    assert str(excinfo.value) == '1'

    assert out == 'ERROR: "log_dir" is missing in the config.\n'


def test_check_plugin_abort(capsys):
    with pytest.raises(SystemExit):
        runner.check_plugin('foobar')

    out, _ = capsys.readouterr()

    assert out == 'ERROR: Plugin "foobar" could not be found.\n'


@patch('dothebackup.runner.sys')
@patch('dothebackup.runner.Path')
def test_check_if_already_running(path_mock, sys_mock):
    path_mock.return_value.exists.return_value = False

    assert runner.check_if_already_running() is None

    sys_mock.assert_not_called()


@patch('dothebackup.runner.Path')
def test_check_if_already_running_abort(path_mock, capsys):
    path_mock.return_value.exists.return_value = True

    with pytest.raises(SystemExit) as excinfo:
        runner.check_if_already_running()

    out, _ = capsys.readouterr()

    assert str(excinfo.value) == '1'

    assert out == 'ERROR: Other DoTheBackup process is running.\n'


@pytest.mark.parametrize('input,expected', [
    ({'test': [['rsync', '-av', '--delete', '/foo/bar/', '/bumm/zack']]},
     'test\n----\n\n  * rsync -av --delete /foo/bar/ /bumm/zack\n\n\n')
])
def test_run_commands_test(input, expected, capsys):
    runner.run_commands(input, test=True, log_dir='/foo/bar', log_keep=10)

    out, err = capsys.readouterr()

    assert out == expected


def test_enabled_missing_in_builder(capsys):
    with pytest.raises(SystemExit) as excinfo:
        runner.builder(
            {
                'log_dir': '/logs',
                'backup': {
                    'test': {
                        'type': 'rsync',
                        'mode': 'once',
                        'source': '/source',
                        'destination': '/destination'
                    }
                }
            },
            name=None
        )

    out, err = capsys.readouterr()

    assert str(excinfo.value) == '1'

    assert out == 'ERROR: "enabled" is missing in the config.\n'


@patch('dothebackup.runner.sys.exit')
def test_enabled_missing_in_builder_exit_code(mock_sys):
    mock_sys.side_effect = SystemExit

    with pytest.raises(SystemExit):

        runner.builder(
            {
                'log_dir': '/logs',
                'backup': {
                    'test': {
                        'type': 'rsync',
                        'mode': 'once',
                        'source': '/source',
                        'destination': '/destination'
                    }
                }
            },
            name=None
        )

    mock_sys.assert_called_with(1)


def test_builder_name():
    config = {
        'backup': {
            'test1': {
                'type': 'tar',
                'source': ['/foo/bar'],
                'destination': '/zack/bumm.tar'
            },
            'test2': {
                'type': 'tar',
                'enabled': True,
                'source': ['/foo/bar'],
                'destination': '/zack/bumm.tar'
            }
        }
    }

    expected = {
        'test1': [['tar', '-vcp', '-f', '/zack/bumm.tar', '/foo/bar']]
    }

    assert runner.builder(config, name='test1') == expected


def test_builder_name_name_not_found(capsys):
    config = {
        'backup': {
            'test1': {
                'type': 'tar',
                'source': ['/foo/bar'],
                'destination': '/zack/bumm.tar'
            },
            'test2': {
                'type': 'tar',
                'enabled': True,
                'source': ['/foo/bar'],
                'destination': '/zack/bumm.tar'
            }
        }
    }

    with pytest.raises(SystemExit):
        runner.builder(config, name='test3')

    out, err = capsys.readouterr()

    assert out == 'ERROR: "test3" could not be found in config.\n'


@pytest.mark.parametrize('input,expected', [
    ({
        'backup': {
            'test': {
                'type': 'tar',
                'enabled': True,
                'days': ['01'],
                'source': ['/foo/bar'],
                'destination': '/zack/bumm/zack/bumm.tar'
            }
        }
    }, {}),
    ({
        'backup': {
            'test': {
                'type': 'tar',
                'enabled': True,
                'days': ['00'],
                'source': ['/foo/bar'],
                'destination': '/zack/bumm.tar'
            }
        }
    }, {'test': [['tar', '-vcp', '-f', '/zack/bumm.tar', '/foo/bar']]})
])
def test_builder_date(input, expected, today_is_00):
    assert runner.builder(input, name=None) == expected


@pytest.mark.parametrize('input,expected', [
    ({
        'backup': {
            'test': {
                'type': 'tar',
                'enabled': True,
                'days': ['01'],
                'source': ['/foo/bar'],
                'destination': '/zack/bumm/zack/bumm.tar'
            }
        }
    }, {})
])
def test_builder_date_skipping(input, expected, capsys, today_is_00):
    '''Testing stdout print on skipping date.'''
    assert runner.builder(input, name=None) == expected


@patch('dothebackup.runner.LOG.info')
def test_builder_not_enabled(mock_log):
    runner.builder(
        {
            'log_dir': '/logs',
            'backup': {
                'test': {
                    'type': 'rsync',
                    'mode': 'once',
                    'enabled': False,
                    'source': '/source',
                    'destination': '/destination'
                }
            }
        },
        name=None
    )

    mock_log.assert_called_with('skipping %s', 'test')
