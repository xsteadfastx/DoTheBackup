import pytest


@pytest.fixture(autouse=True)
def mysqldump_executable(monkeypatch):
    monkeypatch.setattr('dothebackup.plugins.spawn.find_executable',
                        lambda x: '/usr/bin/slapcat')


@pytest.fixture(autouse=True)
def git_executable(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.plugins.spawn.find_executable',
        lambda x: '/usr/bin/git')


@pytest.mark.parametrize('input,expected', [
    ({
        'type': 'slapcat',
        'mode': 'once',
        'destination': '/foo/bar'
    }, [['slapcat', '-l', '/foo/bar/backup.ldif']]
    ),
    ({
        'type': 'slapcat',
        'mode': 'git',
        'destination': '/foo/bar'
    }, [['cd', '/foo/bar', '&&', 'git', 'init'],
        ['slapcat', '-l', '/foo/bar/backup.ldif'],
        ['cd', '/foo/bar', '&&', 'git', 'add', 'backup.ldif',
         '&&',
         'git', 'commit', '-m', '"new export"']]
    )
])
def test_main_nothing_there_yet(input, expected, nothing_to_commit, plugins):
    assert plugins['slapcat'](input) == expected


def test_main_git_already_cloned_new_dump(tmpdir, something_to_commit,
                                          plugins):
    tmpdir.mkdir('.git')

    input = {
        'type': 'slapcat',
        'mode': 'git',
        'destination': str(tmpdir)
    }

    expected = [
        ['slapcat', '-l', '{}/backup.ldif'.format(str(tmpdir))],
        ['cd', str(tmpdir),
         '&&',
         'git', 'add', 'backup.ldif',
         '&&',
         'git', 'commit', '-m', '"new export"']
    ]

    assert plugins['slapcat'](input) == expected


def test_main_git_already_cloned_nothing_new(tmpdir, nothing_to_commit,
                                             plugins):
    tmpdir.mkdir('.git')

    input = {
        'type': 'slapcat',
        'mode': 'git',
        'destination': str(tmpdir)
    }

    expected = [
        ['slapcat', '-l', '{}/backup.ldif'.format(str(tmpdir))],
    ]

    assert plugins['slapcat'](input) == expected
