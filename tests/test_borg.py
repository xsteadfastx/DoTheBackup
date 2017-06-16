import pendulum

import pytest


@pytest.fixture
def borg_found(monkeypatch):
    monkeypatch.setattr(
        'dothebackup.plugins.spawn.find_executable',
        lambda x: '/usr/bin/borg'
    )


@pytest.mark.parametrize('config,expected', [
    (
        {
            'type': 'borg',
            'source': [
                '/etc',
                '/srv',
            ],
            'destination': '/media/backup/foo'
        },
        [
            [
                'BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes',
                'borg', 'create', '-v', '--stats',
                '{}::{}'.format(
                    '/media/backup/foo',
                    pendulum.now().format('%Y-%m-%d-%H-%M')
                ),
                '/etc',
                '/srv'
            ]
        ]
    ),
    (
        {
            'type': 'borg',
            'source': [
                '/etc',
                '/srv',
                '/home'
            ],
            'destination': '/media/backup/foo',
            'exclude': [
                '/home/user/Downloads'
            ]
        },
        [
            [
                'BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes',
                'borg', 'create', '-v', '--stats',
                '{}::{}'.format(
                    '/media/backup/foo',
                    pendulum.now().format('%Y-%m-%d-%H-%M')
                ),
                '/etc',
                '/srv',
                '/home',
                '--exclude /home/user/Downloads'
            ]
        ]
    ),
    (
        {
            'type': 'borg',
            'source': [
                '/etc',
                '/srv',
                '/home'
            ],
            'destination': '/media/backup/foo',
            'exclude': [
                '/home/user/Downloads'
            ],
            'keep': {
                'daily': 7,
                'weekly': 4,
                'monthly': 6
            }
        },
        [
            [
                'BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes',
                'borg', 'create', '-v', '--stats',
                '{}::{}'.format(
                    '/media/backup/foo',
                    pendulum.now().format('%Y-%m-%d-%H-%M')
                ),
                '/etc',
                '/srv',
                '/home',
                '--exclude /home/user/Downloads'
            ],
            [
                'borg', 'prune', '-v', '--list',
                '/media/backup/foo',
                '--keep-daily=7',
                '--keep-weekly=4',
                '--keep-monthly=6',
            ]
        ]
    ),
    (
        {
            'type': 'borg',
            'source': [
                '/etc',
            ],
            'destination': '/media/backup/foo',
            'exclude': [
                '/home/user/Downloads'
            ],
            'check': True,
        },
        [
            [
                'BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes',
                'borg', 'create', '-v', '--stats',
                '{}::{}'.format(
                    '/media/backup/foo',
                    pendulum.now().format('%Y-%m-%d-%H-%M')
                ),
                '/etc',
                '--exclude /home/user/Downloads'
            ],
            [
                'borg', 'check', '/media/backup/foo'
            ]
        ]
    ),
    (
        {
            'type': 'borg',
            'source': [
                '/etc',
            ],
            'destination': '/media/backup/foo',
            'exclude': [
                '/home/user/Downloads'
            ],
            'check': False,
        },
        [
            [
                'BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes',
                'borg', 'create', '-v', '--stats',
                '{}::{}'.format(
                    '/media/backup/foo',
                    pendulum.now().format('%Y-%m-%d-%H-%M')
                ),
                '/etc',
                '--exclude /home/user/Downloads'
            ],
        ]
    )

])
def test_main(config, expected, borg_found, plugins):
    assert plugins['borg'](config) == expected
