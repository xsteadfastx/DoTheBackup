github
======

This plugin gets a users public repositories from the `github`_ API and clones them if needed. Else it will go through all cloned repositories and do a ``git pull``.

.. _github: https://github.com

Dependencies
------------

- **git**

Configuration
-------------

A list of required configuration keys:

- **username**:
  Needs to be a valid github username
- **destination**

Here's an example::

    log_dir: /var/log/dothebackup
    backup:
      mygithubrepos:
        type: github
        enabled: yes
        username: xsteadfastx
        destination: /media/backup/github
