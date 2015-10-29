Usage
=====

::

    Usage: dothebackup [OPTIONS] CONFIGFILE

      Commandline interface.

    Options:
      --test     Only prints the created commands that would be used.
      --version  Show the version and exit.
      --help     Show this message and exit.


First you have to create a config file. Its formatted in `YAML`_. The required keys are:

- **log_dir**:
  The destination where the logs will be saved.
- **backup**:
  Here you define all the things you want to backup.

Be sure that you have the key ``enabled`` set to ``true``. Else that part of the config will be ignored.

You also can use the option ``--test`` to get all commands print instead of running them.

Example
-------

::

    log_dir: /var/log/dothebackup
    backup:
      my_documents:
        type: rsync
        enabled: true
        mode: month
        source: /home/myuser/documents
        destination: /media/backup/documents

      music:
        type: rsync
        enabled: true
        mode: once
        source: /home/myuser/Music
        destination: /media/backup/Music

      repos:
        type: github
        enabled: true
        username: xsteadfastx
        destination: /media/backup/repos

.. _YAML: https://de.wikipedia.org/wiki/YAML
