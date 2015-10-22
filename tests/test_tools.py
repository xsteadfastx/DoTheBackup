import pytest

from dothebackup import tools


@pytest.mark.parametrize('input,expected', [
    ('/foo//bar', '/foo/bar'),
    ('//foo', '/foo')
])
def test_absolutenormpath(input, expected):
    tools.absolutenormpath(input) == expected
