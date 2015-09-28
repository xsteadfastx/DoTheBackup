import pytest


@pytest.fixture
def rsync_found(monkeypatch):
    monkeypatch.setattr('dothebackup.plugins.spawn.find_executable',
                        lambda x: '/usr/bin/rsync')


@pytest.fixture
def rsync_not_found(monkeypatch):
    monkeypatch.setattr('dothebackup.plugins.spawn.find_executable',
                        lambda x: None)
