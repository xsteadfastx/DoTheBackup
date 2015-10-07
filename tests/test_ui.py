import pytest

from dothebackup import ui


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
        ui.check_config_keys(config, ['log_dir', 'backup'])

    out, err = capsys.readouterr()

    assert out == 'ERROR: "log_dir" is missing in the config.\n'


def test_check_plugin_abort(capsys):
    with pytest.raises(SystemExit):
        ui.check_plugin('foobar')

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

    ui.builder(config)

    out, err = capsys.readouterr()

    assert out == 'skipping test\n'


@pytest.mark.parametrize('input,expected', [
    ({'test': [['rsync', '-av', '--delete', '/foo/bar/', '/bumm/zack']]},
     'test\n----\n\n  * rsync -av --delete /foo/bar/ /bumm/zack\n\n\n')
])
def test_runner_test(input, expected, capsys):
    ui.runner(input, True, '/foo/bar')

    out, err = capsys.readouterr()

    assert out == expected


def test_enabled_missing_in_builder(capsys):
    with pytest.raises(SystemExit):
        ui.builder({
            'log_dir': '/logs',
            'backup': {
                'test': {
                    'type': 'rsync',
                    'mode': 'once',
                    'source': '/source',
                    'destination': '/destination'
                }
            }
        })

    out, err = capsys.readouterr()

    assert out == 'ERROR: "enabled" is missing in the config.\n'
