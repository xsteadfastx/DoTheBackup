DoTheBackup
===========

Backups files in a directory names after the backup day. It tries to use hardlinks from the day before to reduce space. You can also use a list of dirs as input. 

```
Usage:
    DoTheBackup.py do <from> <to>
    DoTheBackup.py do -f <file>

Options:
    do          syncs dir to dir
    do -f       reads backup dirs from file
```
