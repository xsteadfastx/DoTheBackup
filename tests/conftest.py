from dothebackup.plugins import load_plugins

import pytest

import yaml


@pytest.fixture
def plugins():
    return load_plugins()


@pytest.fixture
def rsync_found(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.plugins.spawn.find_executable',
        lambda x: '/usr/bin/rsync'
    )


@pytest.fixture
def rsync_not_found(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.plugins.spawn.find_executable',
        lambda x: None
    )


@pytest.yield_fixture
def fake_data(tmpdir):
    source_dir = tmpdir.mkdir('source')
    for i in range(10):
        p = source_dir.join('{}.txt'.format(i))
        p.write('THIS IS A TEST!')

    tmpdir.mkdir('destination')

    yield tmpdir


@pytest.fixture
def today_is_00(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.utils.today',
        lambda: '00'
    )


@pytest.fixture
def something_to_commit(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.utils.subprocess.check_output',
        lambda path, shell: b'A  foo/bar.py'
    )


@pytest.fixture
def nothing_to_commit(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.utils.subprocess.check_output',
        lambda path, shell: b''
    )


@pytest.fixture
def config(tmpdir):
    config = {
        'logs': {
            'dir': tmpdir.mkdir('logs').strpath,
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
    }

    # write config
    config_file = tmpdir.join('config.yaml')
    config_file.write(
        yaml.dump(config, default_flow_style=False)
    )

    return config_file.strpath
