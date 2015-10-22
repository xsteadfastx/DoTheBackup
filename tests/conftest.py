import pytest


@pytest.fixture
def rsync_found(monkeypatch):
    monkeypatch.setattr('dothebackup.plugins.spawn.find_executable',
                        lambda x: '/usr/bin/rsync')


@pytest.fixture
def rsync_not_found(monkeypatch):
    monkeypatch.setattr('dothebackup.plugins.spawn.find_executable',
                        lambda x: None)


@pytest.yield_fixture
def fake_data(tmpdir):
    source_dir = tmpdir.mkdir('source')
    for i in range(10):
        p = source_dir.join('{}.txt'.format(i))
        p.write('THIS IS A TEST!')

    tmpdir.mkdir('destination')

    yield tmpdir
