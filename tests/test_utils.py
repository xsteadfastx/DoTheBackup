# pylint: disable=missing-docstring, redefined-builtin, unused-argument

from pathlib import Path
from unittest.mock import patch

import pytest

from dothebackup import utils


@pytest.mark.parametrize('input,expected', [
    ('/foo//bar', '/foo/bar'),
    ('//foo', '//foo')
])
def test_absolutenormpath(input, expected):
    assert utils.absolutenormpath(input) == expected


def test_git_cloned_yet(tmpdir):
    assert utils.git_cloned_yet(str(tmpdir)) is False

    # create .git dir
    tmpdir.mkdir('.git')

    assert utils.git_cloned_yet(str(tmpdir)) is True


def test_git_something_to_commit(something_to_commit):
    assert utils.git_something_to_commit('/foo/bar') is True


def test_git_nothing_to_commit(nothing_to_commit):
    assert utils.git_something_to_commit('/foo/bar') is False


@pytest.mark.parametrize('input,expected', [
    (
        [0, 0, 1],
        1
    ),
    (
        [0, 0, 0, 0, 0],
        0
    )
])
def test_return_code(input, expected):
    assert utils.return_code(input) == expected


@patch('dothebackup.utils.Path')
def test_pidfile(mock_path, tmpdir):
    pidfile = tmpdir.join('dothebackup.pid')
    mock_path.return_value = Path(pidfile.strpath)

    with utils.pidfile():
        assert pidfile.exists() is True

    assert pidfile.exists() is False


@patch('dothebackup.utils.Path')
def test_pidfile_finally(mock_path, tmpdir):
    pidfile = tmpdir.join('dothebackup.pid')
    mock_path.return_value = Path(pidfile.strpath)

    with pytest.raises(SystemExit):
        with utils.pidfile():
            raise SystemExit

    assert pidfile.exists() is False
