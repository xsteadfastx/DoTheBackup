# pylint: disable=invalid-name, missing-docstring, unused-argument
# pylint: disable=redefined-outer-name

import os

import pytest

from dothebackup.logger import Logger


@pytest.mark.parametrize('logfiles,expected', [
    (
        [
            'foo.log',
            'foo.log.0001',
            'foo.log.0002',
            'bar.log'
        ],
        [
            'foo.log.0002',
            'foo.log.0001',
            'foo.log'
        ]
    )
])
def test__old_logs(logfiles, expected, tmpdir):
    # pylint: disable=protected-access
    for logfile in logfiles:
        tmpdir.join(logfile).write('foo')

    logger = Logger(str(tmpdir.realpath()), 'foo', 10)

    assert logger._old_logs() == expected


@pytest.mark.parametrize('logfiles,expected', [
    (
        [],
        []
    ),
    (
        [
            'foo.log'
        ],
        [
            'foo.log.0001'
        ]
    ),
    (
        [
            'foo.log',
            'foo.log.0001',
            'foo.log.0002',
            'foo.log.0003',
            'foo.log.0004',
            'foo.log.0005'
        ],
        [
            'foo.log.0006',
            'foo.log.0005',
            'foo.log.0004',
            'foo.log.0003',
            'foo.log.0002',
            'foo.log.0001',
        ]
    ),
    (
        [
            'foo.log.0010'
        ],
        []
    )
])
def test_rotate(logfiles, expected, tmpdir):
    for logfile in logfiles:
        tmpdir.join(logfile).write('foo')

    logger = Logger(str(tmpdir.realpath()), 'foo', 10)

    logger.rotate()

    logs = list(reversed(sorted(os.listdir(str(tmpdir.realpath())))))

    assert logs == expected


def test_logfile(tmpdir):
    log_dir = str(tmpdir.join('logs').realpath())

    logger = Logger(log_dir, 'foo', 10)
    logger.create_log_dir()

    with logger.logfile() as logfile:
        logfile.write('foo')

    with open(
        os.path.join(
            log_dir,
            'foo.log'
        )
    ) as f:

        assert f.read() == 'foo'
