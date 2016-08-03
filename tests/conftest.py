import pytest

from dothebackup.plugins import load_plugins


@pytest.fixture
def plugins():
    return load_plugins()


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


@pytest.fixture
def today_is_00(monkeypatch):
    monkeypatch.setattr('dothebackup.tools.today',
                        lambda: '00')


@pytest.fixture
def something_to_commit(monkeypatch):
    monkeypatch.setattr('dothebackup.tools.subprocess.check_output',
                        lambda path, shell: b'A  foo/bar.py')


@pytest.fixture
def nothing_to_commit(monkeypatch):
    monkeypatch.setattr('dothebackup.tools.subprocess.check_output',
                        lambda path, shell: b'')
