import os
import pytest

from dothebackup.logger import Logger


@pytest.mark.parametrize('logfiles,expected', [
    (
        [
            'foo.log',
            'foo.log.1',
            'foo.log.2',
            'bar.log'
        ],
        [
            'foo.log.2',
            'foo.log.1',
            'foo.log'
        ]
    )
])
def test__old_logs(logfiles, expected, tmpdir):
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
            'foo.log.1'
        ]
    ),
    (
        [
            'foo.log',
            'foo.log.1',
            'foo.log.2',
            'foo.log.3',
            'foo.log.4',
            'foo.log.5'
        ],
        [
            'foo.log.6',
            'foo.log.5',
            'foo.log.4',
            'foo.log.3',
            'foo.log.2',
            'foo.log.1',
        ]
    ),
    (
        [
            'foo.log.10'
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

    with logger.logfile() as logfile:
        logfile.write('foo')

    with open(
            os.path.join(
                log_dir,
                'foo.log'
            )
    ) as f:

        assert f.read() == 'foo'
