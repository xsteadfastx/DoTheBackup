import pytest

from dothebackup import PLUGINS


@pytest.fixture
def dot_git_exists(monkeypatch):
    monkeypatch.setattr('dothebackup.tools.git_cloned_yet',
                        lambda x: True)


@pytest.fixture(autouse=True)
def git_executable(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.plugins.spawn.find_executable',
        lambda x: '/usr/bin/git')


@pytest.mark.parametrize('source', [
    'https://github.com/xsteadfastx/DoTheBackup.git',
    'git@github.com:xsteadfastx/DoTheBackup.git'
])
def test_main_not_cloned_yet(source):
    config = {
        'type': 'git',
        'source': source,
        'destination': '/foo/bar'
    }

    assert PLUGINS['git'](config) == [
        ['git', 'clone', source, '/foo/bar'],
        ['cd', '/foo/bar', '&&', 'git', 'pull']
    ]


@pytest.mark.parametrize('source', [
    'https://github.com/xsteadfastx/DoTheBackup.git',
    'git@github.com:xsteadfastx/DoTheBackup.git'
])
def test_main_cloned(source, dot_git_exists):
    config = {
        'type': 'git',
        'source': source,
        'destination': '/foo/bar'
    }

    assert PLUGINS['git'](config) == [
        ['cd', '/foo/bar', '&&', 'git', 'pull']
    ]
