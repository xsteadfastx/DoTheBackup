'''
Usage:
    DoTheBackup.py do <from> <to>
    DoTheBackup.py do -f <file>

Options:
    do          syncs dir to dir
    do -f       reads backup dirs from file
'''
import datetime
import subprocess
import os.path
from docopt import docopt


arguments = docopt(__doc__)

TODAY = datetime.date.today().strftime('%d')
YESTERDAY = (datetime.date.today() - datetime.timedelta(1)).strftime('%d')


def do(backup_from, backup_to):
    backup_from = os.path.abspath(os.path.normpath(backup_from))
    backup_to_today = os.path.join(os.path.abspath(os.path.normpath(backup_to)), TODAY)
    link_dest = os.path.join(os.path.abspath(os.path.normpath(backup_to)), YESTERDAY)

    cmd = ['rsync', '-av', '--delete', '--link-dest=' + link_dest, backup_from,
           backup_to_today]

    if not os.path.exists(backup_to_today):
        os.makedirs(backup_to_today)

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)

    with open(backup_to + '/' + os.path.basename(backup_from) + '.log', 'w') as f:
        for i in proc.stdout:
            f.write(i)
        proc.wait()
        f.write('Exit Code: ' + str(proc.returncode))


def do_filelist():
    filelist = os.path.abspath(os.path.normpath(arguments['<file>']))

    with open(filelist) as f:
        for i in f.readlines():
            backup_from = os.path.abspath(i.split()[0])
            backup_to = os.path.abspath(i.split()[1])

            do(backup_from, backup_to)


def main():
    if arguments['do']:
        if arguments['-f']:
            do_filelist()
        else:
            do(arguments['<from>'], arguments['<to>'])


if __name__ == '__main__':
    main()
