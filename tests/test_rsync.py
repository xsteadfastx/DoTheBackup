# pylint: disable=missing-docstring, invalid-name, unused-argument
# pylint: disable=redefined-builtin

import os
import shutil
from unittest.mock import patch

import pendulum
import pytest
import yaml

import helper
from dothebackup import runner

# GLOBAL VARIABLES
# ----------------
now = pendulum.utcnow()

today_day_of_month = now.format('%d')
yesterday_day_of_month = now.yesterday().format('%d')

today_day_of_week = now.format('%w')
yesterday_day_of_week = now.yesterday().format('%w')

once_input = {
    'type': 'rsync',
    'mode': 'once',
    'source': '/foo/bar',
    'destination': '/bumm/zack'
}

once_expected = [
    ['rsync', '-av', '--delete', '/foo/bar/', '/bumm/zack']
]

once_include_input = {
    'type': 'rsync',
    'mode': 'once',
    'source': '/foo/bar',
    'destination': '/bumm/zack',
    'include': ['eins', 'zwei']
}

once_include_expected = [
    ['rsync', '-av', '--delete', '--include=eins', '--include=zwei',
     '/foo/bar/', '/bumm/zack']
]

once_exclude_input = {
    'type': 'rsync',
    'mode': 'once',
    'source': '/foo/bar',
    'destination': '/bumm/zack',
    'include': ['eins', 'zwei'],
    'exclude': ['drei', 'vier']
}

once_exclude_expected = [
    ['rsync', '-av', '--delete', '--exclude=drei', '--exclude=vier',
     '--include=eins', '--include=zwei', '/foo/bar/', '/bumm/zack']
]

once_missing_mode = {
    'type': 'rsync',
    'source': '/foo/bar',
    'destination': '/bumm/zack'
}

week_input = {
    'type': 'rsync',
    'mode': 'week',
    'source': '/foo/bar',
    'destination': '/bumm/zack'
}

week_expected = [
    ['rsync', '-av', '--delete',
     '--link-dest=../{}'.format(yesterday_day_of_week),
     '/foo/bar/', '/bumm/zack/{}'.format(today_day_of_week)]
]

month_input = {
    'type': 'rsync',
    'mode': 'month',
    'source': '/foo/bar',
    'destination': '/bumm/zack'
}

month_expected = [
    ['rsync', '-av', '--delete',
     '--link-dest=../{}'.format(yesterday_day_of_month),
     '/foo/bar/', '/bumm/zack/{}'.format(today_day_of_month)]
]

once_ssh_input = {
    'type': 'rsync',
    'mode': 'once',
    'source': '/foo/bar',
    'destination': 'foo@bar.com:/bumm/zack'
}

once_ssh_expected = [
    ['rsync', '-av', '--delete', '-e ssh', '/foo/bar/',
     'foo@bar.com:/bumm/zack']
]


# CONFIG CREATION
# ---------------
def config_once(temp_dir):
    return {
        'logs': {
            'dir': os.path.join(temp_dir, 'logs'),
            'keep': 10,
        },
        'backup': {
            'test-once': {
                'type': 'rsync',
                'mode': 'once',
                'enabled': 'true',
                'source': os.path.join(temp_dir, 'source'),
                'destination': os.path.join(temp_dir, 'destination')
            }
        }
    }


def config_link_dest(temp_dir):
    return {
        'logs': {
            'dir': os.path.join(temp_dir, 'logs'),
            'keep': 10,
        },
        'backup': {
            'test-once': {
                'type': 'rsync',
                'mode': 'month',
                'enabled': 'true',
                'source': os.path.join(temp_dir, 'source'),
                'destination': os.path.join(temp_dir, 'destination')
            }
        }
    }


# TESTS
# -----
@patch('dothebackup.runner.pidfile', autospec=True)
@patch('dothebackup.runner.check_if_already_running')
def test_mode_once(check_if_already_running_mock, pidfile_mock, fake_data):
    check_if_already_running_mock.return_value = False

    with pytest.raises(SystemExit) as excinfo:

        # write test config
        fake_data.join('test.yml').write(
            yaml.dump(
                config_once(str(fake_data))
            )
        )

        # run it
        with open(str(fake_data.join('test.yml')), 'r') as f:
            runner.get_started(f, name=None, test=False)

        # check filelist
        source_filelist = os.listdir(os.path.join(str(fake_data), 'source'))
        destination_filelist = os.listdir(
            os.path.join(str(fake_data), 'destination'))

        assert source_filelist == destination_filelist

    assert str(excinfo.value) == '0'


@patch('dothebackup.runner.pidfile', autospec=True)
@patch('dothebackup.runner.check_if_already_running')
def test_mode_month(check_if_already_running_mock, pidfile_mock, fake_data):
    check_if_already_running_mock.return_value = False

    with pytest.raises(SystemExit) as excinfo:

        # write test config
        fake_data.join('test.yml').write(
            yaml.dump(config_link_dest(str(fake_data))))

        with open(str(fake_data.join('test.yml')), 'r') as f:
            # run for the first time
            runner.get_started(f, name=None, test=False)

        # move the today dir to yesterday dir
        shutil.move(
            str(fake_data.join('destination', today_day_of_month)),
            str(fake_data.join('destination', yesterday_day_of_month))
        )

        with open(str(fake_data.join('test.yml')), 'r') as f:
            # run backup again
            runner.get_started(f, name=None, test=False)

        # today inode list
        today_dir = str(fake_data.join('destination', today_day_of_month))
        today_filelist = [
            os.path.join(today_dir, i)
            for i in os.listdir(today_dir)
        ]
        today_inodes = helper.inode_list(today_filelist)

        # yesterday inode list
        yesterday_dir = str(
            fake_data.join('destination', yesterday_day_of_month)
        )

        yesterday_filelist = [
            os.path.join(yesterday_dir, i)
            for i in os.listdir(yesterday_dir)
        ]

        yesterday_inodes = helper.inode_list(yesterday_filelist)

        assert today_inodes == yesterday_inodes

    assert str(excinfo.value) == '0'


@pytest.mark.parametrize('input,expected', [
    (once_input, once_expected),
    (week_input, week_expected),
    (month_input, month_expected),
    (once_include_input, once_include_expected),
    (once_exclude_input, once_exclude_expected),
    (once_ssh_input, once_ssh_expected)
])
def test_main(input, expected, rsync_found, plugins):
    assert plugins['rsync'](input) == expected
