rsync
=====

This plugin uses `rsync`_ to sync directories local and remote.

.. _rsync: https://en.wikipedia.org/wiki/Rsync

Dependencies
------------

- **rsync**
- **ssh**:
  This is needed for remote syncs.

Configuration
-------------

A list of required configuration keys:

- **source**:
  A directory that should be synced.
- **destination**:
  The directory the backup should be synced to.

Its also needed to define a ``mode``. Here is a list:

- **once**:
  Syncs one to one. It also deleted files on destination that are not there anymore.
- **week**:
  Keeps one week. It stores the files in a numbered day directory and uses hardlinks to link to the files that are not changed from the day before.
- **month**:
  Keeps one month. it stores the files for one month in a day numbered directory and works with hardlinks just like the week mode.

It supports rsync ``exclude`` and ``include`` patterns as list.

Here's an example::

    log_dir: /var/log/dothebackup
    backup:
      my_documents:
        type: rsync
        enabled: yes
        mode: month
        source: /home/myuser/documents
        destination: /media/backup/documents
        exclude:
          - foo
          - bar
        include:
          - importantdir

This would save the source to ``/media/backup/documents/27`` for example and rotate for one month with day numbers.

It supports ssh for transfering data to remote hosts. For example::

    log_dir: /var/log/dothebackup
    backup:
      my_documents:
        type: rsync
        enabled: yes
        mode: once
        source: /home/myuser/documents
        destination: ssh://foo@remotehost:/media/backup/documents

Be sure that you are allowed to connect and ssh-keys are exchanged.

API
---

.. automodule:: dothebackup.plugs.rsync
     :members:
