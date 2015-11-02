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

    with pytest.raises(SystemExit):
        runner.check_config_keys(config, ['log_dir', 'backup'])

    out, err = capsys.readouterr()

    assert out == 'ERROR: "log_dir" is missing in the config.\n'


def test_check_plugin_abort(capsys):
    with pytest.raises(SystemExit):
        runner.check_plugin('foobar')

    out, err = capsys.readouterr()

    assert out == 'ERROR: Plugin "foobar" could not be found.\n'


def test_builder_skipping(capsys):
    config = {
        'backup': {
            'test': {
                'type': 'rsync',
                'mode': 'once',
                'enabled': False,
                'source': '/foo/bar',
                'destination': '/zack/bumm'
            }
        }
    }

    runner.builder(config, name=None)

    out, err = capsys.readouterr()

    assert out == 'skipping test\n'


@pytest.mark.parametrize('input,expected', [
    ({'test': [['rsync', '-av', '--delete', '/foo/bar/', '/bumm/zack']]},
     'test\n----\n\n  * rsync -av --delete /foo/bar/ /bumm/zack\n\n\n')
])
def test_runner_test(input, expected, capsys):
    runner.run_commands(input, test=True, log_dir='/foo/bar')

    out, err = capsys.readouterr()

    assert out == expected


def test_enabled_missing_in_builder(capsys):
    with pytest.raises(SystemExit):
        runner.builder({
            'log_dir': '/logs',
            'backup': {
                'test': {
                    'type': 'rsync',
                    'mode': 'once',
                    'source': '/source',
                    'destination': '/destination'
                }
            }
        }, name=None)

    out, err = capsys.readouterr()

    assert out == 'ERROR: "enabled" is missing in the config.\n'


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

    out, err = capsys.readouterr()

    assert out == 'skipping test\n'
