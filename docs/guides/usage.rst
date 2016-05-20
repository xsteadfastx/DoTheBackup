Usage
=====

::

    Usage: dothebackup [OPTIONS] CONFIGFILE

      Commandline interface.

    Options:
      --name TEXT  Run a specific job from the config.
      --test     Only prints the created commands that would be used.
      --version  Show the version and exit.
      --help     Show this message and exit.


First you have to create a config file. Its formatted in `YAML`_. The required keys are:

- **log_dir**:
  The destination where the logs will be saved.
- **backup**:
  Here you define all the things you want to backup.

Be sure that you have the key ``enabled`` set to ``yes``. Else that part of the config will be ignored on a normal run.

You also can use the option ``--test`` to get all commands print instead of running them.

There is a way to trigger a job only on specific days. The key ``days`` is needed for that. Its a list of days like::

    days:
      - 01
      - 15

This would trigger the job on day ``01`` and ``15`` in the month. You need to be sure its a two diget number.

There is a way to trigger only one job from the commandline. Run ``dothebackup`` with the option ``--name`` and the name of the job. This would run this one job and ignore everything else in the config. You dont even need to set ``enabled`` to ``yes``. Its handy if you do from time to time backups to external harddrives and want to define the way the backup should run.

Example
-------

::

    log_dir: /var/log/dothebackup
    backup:
      my_documents:
        type: rsync
        enabled: yes
        mode: month
        source: /home/myuser/documents
        destination: /media/backup/documents

      music:
        type: rsync
        enabled: yes
        mode: once
        source: /home/myuser/Music
        destination: /media/backup/Music

      repos:
        type: github
        enabled: yes
        username: xsteadfastx
        destination: /media/backup/repos
        days:
          - 01
          - 15

.. _YAML: https://de.wikipedia.org/wiki/YAML
