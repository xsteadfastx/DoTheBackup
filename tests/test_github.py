import pytest
import json


@pytest.fixture(autouse=True)
def get_repos(monkeypatch):
    with open('tests/data/github_repos.txt') as f:
        repos = json.loads(f.read())

    monkeypatch.setattr(
        'github.get_repos',
        lambda x: repos)


@pytest.fixture(autouse=True)
def git_executable(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.plugins.spawn.find_executable',
        lambda x: '/usr/bin/git')


def test_main_not_cloned_yet(plugins):
    config = {
        'type': 'github',
        'destination': '/foo/bar',
        'username': 'test_user'
    }

    expected = [
        ['git', 'clone', 'https://github.com/xsteadfastx/ari-verblonshen.git',
         '/foo/bar/ari-verblonshen'],
        ['cd', '/foo/bar/ari-verblonshen', '&&', 'git', 'pull'],
        ['git', 'clone', 'https://github.com/xsteadfastx/art_millionaire.git',
         '/foo/bar/art_millionaire'],
        ['cd', '/foo/bar/art_millionaire', '&&', 'git', 'pull']
    ]

    assert plugins['github'](config) == expected
