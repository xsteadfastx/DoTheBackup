import pytest


once_input = {
    'type': 'rsync',
    'mode': 'once',
    'source': '/foo/bar',
    'destination': '/bumm/zack'
}

once_missing_mode = {
    'type': 'rsync',
    'source': '/foo/bar',
    'destination': '/bumm/zack'
}


@pytest.mark.parametrize('input, expected', [
    (once_missing_mode, 'ERROR: "mode" not in config.\n')
])
def test_required_keys(input, expected, capsys, rsync_found, plugins):
    with pytest.raises(SystemExit):
        plugins['rsync'](input)

    out, err = capsys.readouterr()

    assert out == expected


def test_required_executables(rsync_not_found, capsys, plugins):
    with pytest.raises(SystemExit):
        plugins['rsync'](once_input)

    out, err = capsys.readouterr()

    assert out == 'ERROR: Please install rsync.\n'
