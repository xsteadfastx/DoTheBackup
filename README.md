DoTheBackup
===========

Backups files in a directory names after the backup day. It tries to use hardlinks from the day before to reduce space. you also can use a list of files as input. 

```
Usage:
    DoTheBackup.py do <from> <to>
    DoTheBackup.py do -f <file>

Options:
    do          syncs dir to dir
    do -f       reads backup dirs from file
```
