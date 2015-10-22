Installation
============

pip
---

The easiest way to install dothebackup is to use `pip`_. The only thing you should take care of is that you really use the Python 3 version of pip.

On Ubuntu for example:

1. ``sudo apt-get install python3-pip``
2. ``sudo pip3 install dothebackup``

.. _pip: https://pip.pypa.io/

virtualenv
----------

Living on the edge. You can just pull the `repo`_ and install dothebackup in an `virtualenv`_.

On Ubuntu for example:

1. ``sudo apt-get install python3-virtualenv``
2. ``git clone https://github.com/xsteadfastx/DoTheBackup.git``
3. ``cd DoTheBackup``
4. ``virtualenv env``
5. ``make editable``

Now you should be able to use dothebackup.

.. _repo: https://github.com/xsteadfastx/DoTheBackup
.. _virtualenv: https://virtualenv.pypa.io/
