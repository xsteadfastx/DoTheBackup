Changelog
=========

0.1.8
-----

* Adds finishing date and total runtime to log. Thanks to `derphilipp`_.

.. _derphilipp: https://github.com/xsteadfastx/DoTheBackup/commit/b1a9abe863993993fa9589e3e06937d95606e9af

0.1.7
-----

* Fixes a bug where git something to commit detection fails if git is not initialised yet

0.1.6
-----

* Added :doc:`/plugins/slapcat` plugin.

0.1.5
-----

* Added ``git_cloned_yet`` and ``git_something_to_commit`` function to tools.
* Added :doc:`/plugins/mysql` plugin.

0.1.4
-----

* Restructured code. Splitted the ui and runner parts.
* Testing also against Python versions 3.2, 3.3 and 3.5.
* Added ``name`` option to command line for running only a specific job. Even if its not enabled.
* The config file takes a ``days`` list for a job. Before running it will check the day its running and if its in the list. Else it will skip it.

0.1.3
-----

* Because the Unicode Python2 and Python3 problems i decided to drop support for Python2.
* Added :doc:`/plugins/tar` plugin.
* Created docs.
