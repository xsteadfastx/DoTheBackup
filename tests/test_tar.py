import pytest

from dothebackup import PLUGINS


@pytest.fixture
def tar_found(monkeypatch):
    monkeypatch.setattr('dothebackup.plugins.spawn.find_executable',
                        lambda x: '/bin/tar')


@pytest.mark.parametrize('input,expected', [
    ({'type': 'tar',
      'source': ['/foo/bar'],
      'destination': '/bar/zonk.tar'},
     [['tar', '-vcp', '-f', '/bar/zonk.tar', '/foo/bar']]),
    ({'type': 'tar',
      'source': ['/foo/bar', '/bar/foo'],
      'destination': '/foo/zonk.tar'},
     [['tar', '-vcp', '-f', '/foo/zonk.tar', '/foo/bar', '/bar/foo']]),
    ({'type': 'tar',
      'source': ['/foo/bar'],
      'destination': '/bar/zonk.tar.bz2'},
     [['tar', '-vcp', '-j', '-f', '/bar/zonk.tar.bz2', '/foo/bar']]),
    ({'type': 'tar',
      'source': ['/foo/bar'],
      'destination': '/bar/zonk.tar.xz'},
     [['tar', '-vcp', '-J', '-f', '/bar/zonk.tar.xz', '/foo/bar']]),
    ({'type': 'tar',
      'source': ['/foo/bar'],
      'destination': '/bar/zonk.tar.gz'},
     [['tar', '-vcp', '-z', '-f', '/bar/zonk.tar.gz', '/foo/bar']])
])
def test_main(input, expected, tar_found):
    '''Test created command list.'''
    assert PLUGINS['tar'](input) == expected
