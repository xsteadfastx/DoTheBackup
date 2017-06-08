borg
====

This plugin will perform a `borg`_ backup in a specific repo. It will also run a ``borg prune``-command to clean up old backups.

.. _borg: https://borgbackup.readthedocs.io

Dependencies
------------

- **borg**

Preparation
-----------

Create a borg repository local or on a remote machine::

    borg init -e none /media/backup/my_borg_backup_repo

Configuration
-------------

A list of required configuration keys:

- **source**:
  A list of sources to backup
- **destination**
  A ``borg``-repository to backup to

Here's an example::

    logs:
      dir: /var/log/dothebackup
      keep: 10
    backup:
      my_borg_backup:
        type: borg
        enabled: yes
        source:
            - /etc
            - /home
            - /srv
        destination: /media/backup/my_borg_backup_repo
        exclude:
            - /home/user/Downloads
        keep:
            daily: 7
            weekly: 4
            monthly: 6

It's also possible to use a remote destination::

    destination: ssh://user@remotebox:/media/backup/my_borg_backup_repo

API
---

.. automodule:: dothebackup.plugs.git
     :members:
