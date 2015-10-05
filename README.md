[![Build Status](https://travis-ci.org/xsteadfastx/DoTheBackup.svg?branch=master)](https://travis-ci.org/xsteadfastx/DoTheBackup)
[![Coverage Status](http://img.shields.io/codecov/c/github/xsteadfastx/DoTheBackup.svg)](https://codecov.io/github/xsteadfastx/DoTheBackup)

A small tool to run backups in different ways. Its pluggable.

## Install ##

`pip install dothebackup`

## Usage ##

```
Usage: dothebackup [OPTIONS] CONFIGFILE

  Commandline interface.

Options:
  --test     Only prints the created commands that would be used.
  --version  Show the version and exit.
  --help     Show this message and exit.
```

## Config example ##
```
# destination where the logs will be
log_dir: /var/log/DoTheBackup

# define your backups here
backup:
        my_documents:
		type: rsync
                # "month" means that it will save the backup in daily directories
                # for example: "/media/backup/documents/07"
		mode: month
                enabled: true
                source: /home/user/documents
                destination: /media/backup/documents
                # rsync --exclude patterns here
                exclude:
                        - foo
                        - bar
                # rsync --include patterns here
                include:
                        - very_important_dir

        video:
		type: rsync
                # "once" backups straight in the destination directory
                # for example: "/media/backup/Videos"
                mode: once
                enabled: true
                source: /home/user/Media/Videos
                destination: /media/backup/Videos

	important_stuff:
		type: rsync
		mode: month
		enabled: true
		source: /home/user/very_important
		# this will use ssh to transfer the data over ssh
		destinaton: user@remote:/media/backup/important_stuff
```

## Type plugins ##

### rsync ###
It uses [rsync](https://rsync.samba.org/) to make backups. Be sure you have `rsync` installed.

#### Modes ####
- **once**: Copies one to one.
- **week**: Keeps one week. It stores the files in a numbered day directory and uses hardlinks to link to the files that are not changed from the day before.
- **month**: Keeps one month. it stores the files for one month in a day numbered directory and works with hardlinks just like the week mode.
