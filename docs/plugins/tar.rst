tar
===

This plugin takes a list of sources and puts them into a tarfile.

Dependencies
------------

For simple usage just the normal tar binary is needed. If you want to use some kind of compression, you need to install additional packages.

- **tar**:
  The main command needed for uncompressed archives.
- **xz-utils**:
  For `XZ`_ compressed tarfiles.
- **lbzip2**:
  For `BZIP2`_ compressed tarfiles.

.. _XZ: https://en.wikipedia.org/wiki/Xz
.. _BZIP2: https://en.wikipedia.org/wiki/Bzip2

Configuration
-------------

A list of required configuration keys:

- **source**:
  A list of sources to be included in the archive.
- **destination**:
  The destination file. The extension tells the plugin if a compression is wanted and which or none. Example: ``foo.tar``, ``foo.tar.gz``, ``foo.tar.bzip2``, ``foo.tar.xz``

Here's an example::

    log_dir: /var/log/dothebackup
    backup:
      foo:
        type: tar
        enabled: yes
        source:
          - /home
          - /src
        destination: /media/backup/archives/foo.tar.gz

API
---

.. automodule:: dothebackup.plugs.tar
     :members:
