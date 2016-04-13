from __future__ import absolute_import
import pytest

from dothebackup import PLUGINS


@pytest.fixture(autouse=True)
def mysqldump_executable(monkeypatch):
    monkeypatch.setattr('dothebackup.plugins.spawn.find_executable',
                        lambda x: '/usr/bin/mysqldump')


@pytest.fixture(autouse=True)
def git_executable(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.plugins.spawn.find_executable',
        lambda x: '/usr/bin/git')


@pytest.mark.parametrize('input,expected', [
    ({
        'type': 'mysql',
        'mode': 'once',
        'server': 'localhost',
        'username': 'myuser',
        'password': 'mypassword',
        'database': 'mydatabase',
        'destination': '/foo/bar'
    }, [['mysqldump', '--skip-extended-insert', '--skip-comments',
         '--user=myuser', '--password=mypassword', '--host=localhost',
         'mydatabase', '>', '/foo/bar/mydatabase.sql']]
    ),
    ({
        'type': 'mysql',
        'mode': 'git',
        'server': 'localhost',
        'username': 'myuser',
        'password': 'mypassword',
        'database': 'mydatabase',
        'destination': '/foo/bar'
    }, [['cd', '/foo/bar', '&&', 'git', 'init'],
        ['mysqldump', '--skip-extended-insert', '--skip-comments',
         '--user=myuser', '--password=mypassword', '--host=localhost',
         'mydatabase', '>', '/foo/bar/mydatabase.sql'],
        ['cd', '/foo/bar',
         '&&',
         'git', 'add', 'mydatabase.sql',
         '&&',
         'git', 'commit', '-m', '"new dump"']]
    )
])
def test_main_nothing_there_yet(input, expected, nothing_to_commit):
    assert PLUGINS['mysql'](input) == expected


def test_main_git_already_cloned_new_dump(tmpdir, something_to_commit):
    tmpdir.mkdir('.git')

    input = {
        'type': 'mysql',
        'mode': 'git',
        'server': 'localhost',
        'username': 'myuser',
        'password': 'mypassword',
        'database': 'mydatabase',
        'destination': str(tmpdir)
    }

    expected = [
        ['mysqldump', '--skip-extended-insert', '--skip-comments',
         '--user=myuser', '--password=mypassword', '--host=localhost',
         'mydatabase', '>', '{}/mydatabase.sql'.format(str(tmpdir))],
        ['cd', str(tmpdir),
         '&&',
         'git', 'add', 'mydatabase.sql',
         '&&',
         'git', 'commit', '-m', '"new dump"']
    ]

    assert PLUGINS['mysql'](input) == expected


def test_main_git_already_cloned_nothing_new(tmpdir, nothing_to_commit):
    tmpdir.mkdir('.git')

    input = {
        'type': 'mysql',
        'mode': 'git',
        'server': 'localhost',
        'username': 'myuser',
        'password': 'mypassword',
        'database': 'mydatabase',
        'destination': str(tmpdir)
    }

    expected = [
        ['mysqldump', '--skip-extended-insert', '--skip-comments',
         '--user=myuser', '--password=mypassword', '--host=localhost',
         'mydatabase', '>', '{}/mydatabase.sql'.format(str(tmpdir))],
    ]

    assert PLUGINS['mysql'](input) == expected
