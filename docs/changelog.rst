Changelog
=========


v2.0.0 (2017-11-09)
-------------------

Fix
~~~
- "enabled" missing in config throws exit code 1. [Marvin Steadfast]

Other
~~~~~
- Travis deploy only if $TOXENV is pex. [Marvin Steadfast]
- Creates a pidfile. [Marvin Steadfast]

  This prevents `dothebackup` from running more then once parallel.
- Moving package to src directory. [Marvin Steadfast]
- Using pipenv for development environment and testing. [Marvin
  Steadfast]
- Python 3.3 no longer supported. [Marvin Steadfast]
- Raising coverage. [Marvin Steadfast]
- Testing debug levels of the UI. [Marvin Steadfast]
- Added test for ui. [Marvin Steadfast]


v1.1.1 (2017-06-16)
-------------------

Fix
~~~
- Add typing as dependency. [Marvin Steadfast]


v1.1.0 (2017-06-16)
-------------------
- Print stdout from commands in debug more. [Marvin Steadfast]
- Added borg check command. [Marvin Steadfast]
- Dothebackup return itself an error exit code. [Marvin Steadfast]

  If one job failed it will not just write this to the job logs it also
  will exit with a different exit code.
- Fixing import order in tests. [Marvin Steadfast]
- Added typing and plugin for borg backup. [Marvin Steadfast]
- Switched from ``arrow`` to ``pendulum`` [Marvin Steadfast]


v1.0.2 (2017-01-04)
-------------------
- Replace invalid characters in logging. [Philipp Weißmann]
- Working on Jenkinsfile. [Marvin Steadfast]
- Added Jenkinsfile. [Marvin Steadfast]


v1.0.1 (2016-08-18)
-------------------

Fix
~~~
- Logs finally rotate. [Marvin Steadfast]

  forgot to call the rotate function in the runner and fixed a bug caused
  by the log numbering order. logs are now numbered like::

      foo.log
      foo.log.0001
      foo.log.0002


v1.0.0 (2016-08-18)
-------------------
- Testing and no installations for old python versions. [Marvin
  Steadfast]

  added more python versions for local tox testing. installations on
  python versions < python 3.3 will be aborted in setup.py.
- Logger module. [Marvin Steadfast]

  added logger module for better logging of the jobs stdout. it keeps
  track on rotating old logs and writing to the right logfile.

  the logging part of the config changed. a example::

      logs:
        dir: /var/log/dothebackup
        keep: 10
      backup:
        ...
        ...
        ...

  **keep** defines how many log files to keep.


v0.2.1 (2016-08-15)
-------------------
- Adds log for startup and finishing dothebackup. [Philipp Weißmann]
- New changelog. [Marvin Steadfast]


v0.2.0 (2016-08-08)
-------------------
- More docs and logging. [Marvin Steadfast]
- Better docs and more debug messages. [Marvin Steadfast]
- The runner has debugging messages now. [Marvin Steadfast]
- Test for load_plugins. [Marvin Steadfast]
- Plugin loader not in __init__ and added logging. [Marvin Steadfast]


v0.1.9 (2016-07-29)
-------------------
- 0.1.9 release. [Marvin Steadfast]
- Adds newline seperators to log file. [Philipp Weißmann]


v0.1.8 (2016-07-28)
-------------------
- 0.1.8 release. [Marvin Steadfast]
- Fixes pep violations (line length) [Philipp Weißmann]
- Adds finishing date and total runtime to log. [Philipp Weißmann]
- Fixed typo. [Marvin Steadfast]
- Fixes typo in Readme. [Philipp Weißmann]


v0.1.7 (2016-04-13)
-------------------
- 0.1.7 release. [Marvin Steadfast]

  * Fixes a bug where git something to commit detection fails if git is
  not initialised
- Added forgotten enabled in examples. [Marvin Steadfast]
- Removed support for python 3.2. [Marvin Steadfast]


v0.1.6 (2016-04-12)
-------------------
- Fixed typo in docs. [Marvin Steadfast]
- 0.1.6 release. [Marvin Steadfast]

  * Added slapcat plugin.
- Fixed doc. [Marvin Steadfast]


v0.1.5 (2015-11-12)
-------------------
- 0.1.5 release. [Marvin Steadfast]

  * Added mysql plugin.
  * Added some git tools.
- Fixing travis python 3.5 job. [Marvin Steadfast]


v0.1.4 (2015-11-02)
-------------------
- 0.1.4 release. [Marvin Steadfast]

  * Restructured code. Splitted the ui and runner parts.
  * Testing also against Python versions 3.2, 3.3 and 3.5.
  * Added ``name`` option to command line for running only a specific job.
    Even if its not enabled.
  * The config file takes a ``days`` list for a job. Before running it will
    check the day its running and if its in the list. Else it will skip it.
- Added --test to the docs. [Marvin Steadfast]
- Removed stuff from docs. [Marvin Steadfast]
- Added test_tar fixture. [Marvin Steadfast]


v0.1.3 (2015-10-22)
-------------------
- Added tar plugin, Python 3 only, docs. [Marvin Steadfast]

  Added a plugin that creates tar archives from a list of source
  directories. Dropped Python 2 support because of the UnicodeDecodeErrors
  i dont want to deal with no more. Python 3 should make this more
  futureproof and robust. Also added docs.
- Fix README. [Marvin Steadfast]


v0.1.2 (2015-10-20)
-------------------
- Added github plugin. [Marvin Steadfast]

  Its a plugin to get a users public repositories through the GitHub Api,
  clone them (if not done before) and pulls the changes on every run.
- Fix readme tabs. [Marvin Steadfast]


v0.1.1 (2015-10-07)
-------------------
- Added git plugin. [Marvin Steadfast]

  A simple git plugin to clone a git repo to a destination and run a git
  pull afterwards.
- Using click.File for reading configfile. [Marvin Steadfast]
- Removed old config dist file. [Marvin Steadfast]


v0.1 (2015-10-06)
-----------------
- Added pypi badge to readme. [Marvin Steadfast]
- Added tests for the ui. [Marvin Steadfast]
- Added tests for exclude key. [Marvin Steadfast]
- Moved to codecov. [Marvin Steadfast]
- Removed support for python 3.2. [Marvin Steadfast]
- Rebased everything. [Marvin Steadfast]

  Its now installable through pip. Also it uses plugins now. All you need
  is a plugin that returns a list if commands that get executed. Right now
  only the rsync plugin is there.
- Adds option to keep backups for a week (additional to a month)
  [Philipp Weißmann]
- Still tweaking tox.ini to run also on jenkins smooth. [Marvin
  Steadfast]
- Ignore coverage.xml. [Marvin Steadfast]
- Tests are more verbose now to make jenkins happy. [Marvin Steadfast]
- Changed TOXENV. [Marvin Steadfast]
- Forgot to readd coveralls command. [Marvin Steadfast]
- Test against more python versions. [Marvin Steadfast]
- Moved coverage from .travis.yml to tox.ini to make it simpler and
  cleaner. [Marvin Steadfast]
- Moved test to tests. [Marvin Steadfast]
- Moved from nose to py.test. [Marvin Steadfast]
- Fixed some test and did some refactoring of the tests. [Marvin
  Steadfast]
- Fixed readme layout. [Marvin Steadfast]
- Tests rsync commands. [Marvin Steadfast]
- Subprocess arguments gets tested. [Marvin Steadfast]
- Install rsync for travis testing. [Marvin Steadfast]
- Added .coveragerc. [Marvin Steadfast]
- Better tests through tox and travis. [Marvin Steadfast]
- Some pep8 fix up. [Marvin Steadfast]
- Fixed a bug with the paths when running the tests from a different
  location. [Marvin Steadfast]
- Added first tests. [Marvin Steadfast]
- Almost rewrote everything and added git_mysql type. [Marvin Steadfast]
- Added ssh support. [Marvin Steadfast]
- Added cron shell script. [Marvin Steadfast]
- Complete rewrite. [Marvin Steadfast]
- Fixd readme. [Marvin Steadfast]
- First working version. [Marvin Steadfast]
- Initial commit. [xsteadfastx]


