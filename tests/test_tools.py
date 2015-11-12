import pytest

from dothebackup import tools


@pytest.mark.parametrize('input,expected', [
    ('/foo//bar', '/foo/bar'),
    ('//foo', '/foo')
])
def test_absolutenormpath(input, expected):
    tools.absolutenormpath(input) == expected


def test_git_cloned_yet(tmpdir):
    assert tools.git_cloned_yet(str(tmpdir)) is False

    # create .git dir
    tmpdir.mkdir('.git')

    assert tools.git_cloned_yet(str(tmpdir)) is True


def test_git_something_to_commit(something_to_commit):
    assert tools.git_something_to_commit('/foo/bar') is True


def test_git_nothing_to_commit(nothing_to_commit):
    assert tools.git_something_to_commit('/foo/bar') is False
