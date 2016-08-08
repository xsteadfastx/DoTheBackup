git
===

This plugin clones and pulls a `git`_ repository to the backup machine. First it will check if a repository is already cloned to ``destination`` and if not it will clone and do a ``git pull`` afterwards. On the next runs it will just do a ``git pull``.

.. _git: https://git-scm.com/

Dependencies
------------

- **git**

Configuration
-------------

A list of required configuration keys:

- **source**:
  A repository url to clone from.
- **destination**

Here's an example::

    log_dir: /var/log/dothebackup
    backup:
      my_repository:
        type: git
        enabled: yes
        source: https://github.com/xsteadfastx/DoTheBackup.git
        destination: /media/backup/repos/dothebackup

API
---

.. automodule:: dothebackup.plugs.git
     :members:
