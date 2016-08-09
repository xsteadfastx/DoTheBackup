Changelog
=========

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

- Merge pull request #5 from derphilipp/patch-1. [xsteadfastx]

  Adds newline seperators to log file

- Adds newline seperators to log file. [Philipp Weißmann]

v0.1.8 (2016-07-28)
-------------------

- 0.1.8 release. [Marvin Steadfast]

- Merge pull request #4 from derphilipp/master. [xsteadfastx]

  Adds finishing date and total runtime to log

- Fixes pep violations (line length) [Philipp Weißmann]

- Adds finishing date and total runtime to log. [Philipp Weißmann]

- Fixed typo. [Marvin Steadfast]

- Merge pull request #2 from derphilipp/fix_typo. [xsteadfastx]

  Fixes typo in Readme

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

- Merge pull request #1 from derphilipp/feature/rsync_week.
  [xsteadfastx]

  Adds option to keep backups for a week (additional to a month)

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


