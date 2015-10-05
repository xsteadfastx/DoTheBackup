import arrow
import helper
import os
import pytest
import shutil
import yaml

from dothebackup import PLUGINS, ui


# GLOBAL VARIABLES
# ----------------
now = arrow.utcnow()
today_day_of_month = now.format('DD')
yesterday_day_of_month = now.replace(days=-1).format('DD')
today_day_of_week = now.format('d')
yesterday_day_of_week = now.replace(days=-1).format('d')

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
        'log_dir': os.path.join(temp_dir, 'logs'),
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
        'log_dir': os.path.join(temp_dir, 'logs'),
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


# FIXTURES
# --------
@pytest.yield_fixture
def fake_data(tmpdir):
    source_dir = tmpdir.mkdir('source')
    for i in range(10):
        p = source_dir.join('{}.txt'.format(i))
        p.write('THIS IS A TEST!')

    tmpdir.mkdir('destination')

    yield tmpdir


# TESTS
# -----
def test_mode_once(fake_data):
    # write test config
    fake_data.join('test.yml').write(yaml.dump(config_once(str(fake_data))))

    # run it
    ui.get_started(str(fake_data.join('test.yml')), False)

    # check filelist
    source_filelist = os.listdir(os.path.join(str(fake_data), 'source'))
    destination_filelist = os.listdir(
        os.path.join(str(fake_data), 'destination'))

    assert source_filelist == destination_filelist


def test_mode_month(fake_data):
    # write test config
    fake_data.join('test.yml').write(
        yaml.dump(config_link_dest(str(fake_data))))

    # run for the first time
    ui.get_started(str(fake_data.join('test.yml')), False)

    # move the today dir to yesterday dir
    shutil.move(str(fake_data.join('destination', today_day_of_month)),
                str(fake_data.join('destination', yesterday_day_of_month)))

    # run backup again
    ui.get_started(str(fake_data.join('test.yml')), False)

    # today inode list
    today_dir = str(fake_data.join('destination', today_day_of_month))
    today_filelist = [os.path.join(today_dir, i)
                      for i in os.listdir(today_dir)]
    today_inodes = helper.inode_list(today_filelist)

    # yesterday inode list
    yesterday_dir = str(fake_data.join('destination', yesterday_day_of_month))
    yesterday_filelist = [os.path.join(yesterday_dir, i)
                          for i in os.listdir(yesterday_dir)]
    yesterday_inodes = helper.inode_list(yesterday_filelist)

    assert today_inodes == yesterday_inodes


@pytest.mark.parametrize('input,expected', [
    (once_input, once_expected),
    (week_input, week_expected),
    (month_input, month_expected),
    (once_include_input, once_include_expected),
    (once_exclude_input, once_exclude_expected),
    (once_ssh_input, once_ssh_expected)
])
def test_main(input, expected, rsync_found):
    assert PLUGINS['rsync'](input) == expected


@pytest.mark.parametrize('input, expected', [
    (once_missing_mode, 'ERROR: "mode" not in config.\n')
])
def test_missing_key(input, expected, capsys, rsync_found):
    with pytest.raises(SystemExit):
        PLUGINS['rsync'](input)

    out, err = capsys.readouterr()

    assert out == expected


def test_rsync_missing(rsync_not_found, capsys):
    with pytest.raises(SystemExit):
        PLUGINS['rsync'](once_input)

    out, err = capsys.readouterr()

    assert out == 'ERROR: Please install rsync.\n'


def test_enabled_missing_in_builder(capsys):
    with pytest.raises(SystemExit):
        ui.builder({
            'log_dir': '/logs',
            'backup': {
                'test': {
                    'type': 'rsync',
                    'mode': 'once',
                    'source': '/source',
                    'destination': '/destination'
                }
            }
        })

    out, err = capsys.readouterr()

    assert out == 'ERROR: "enabled" is missing in the config.\n'
