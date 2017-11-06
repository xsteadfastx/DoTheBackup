Installation
============

There are several ways of installing and using dothebackup.

pex
---

You can download a pex-File for every release from the `release`_ page on GitHub. Read more about `pex`_. Its a zipped up virtual environment, with all the dependencies contained, that you can run with just python installed.

1. Be sure you have Python >= 3.4 installed
2. Download pex file from `release`_
3. Move it to a place in your ``$PATH``. For examle ``/usr/local/bin``
4. If you want you can renamse ``dothebackup.pex`` to ``dothebackup``. This makes everything a little more neat

.. _release: https://github.com/xsteadfastx/DoTheBackup/releases
.. _pex: https://github.com/pantsbuild/pex

pip
---

Its also possible to use it with a normal pip command.

On Ubuntu for example:

1. ``sudo apt-get install python3-pip``
2. ``sudo pip3 install dothebackup``

.. _pip: https://pip.pypa.io/

pipenv
------

I use `pipenv`_ to develop. You can use it too to create and manage a virtualenv to run dothebackup in it.

1. Install ``pipenv``
2. ``git clone https://github.com/xsteadfastx/DoTheBackup.git``
3. ``cd DoTheBackup``
4. ``pipenv install --three``
5. ``pipenv run bash -c "pip install -e ."``
6. ``pipenv run dothebackup``

.. _pipenv: https://docs.pipenv.org/

virtualenv
----------

You can just pull the `repo`_ and install dothebackup in an `virtualenv`_.

On Ubuntu for example:

1. ``sudo apt-get install python3-virtualenv``
2. ``git clone https://github.com/xsteadfastx/DoTheBackup.git``
3. ``cd DoTheBackup``
4. ``virtualenv env``
5. ``source env/bin/activate``
6. ``pip install -e .``

Now you should be able to use dothebackup.

.. _repo: https://github.com/xsteadfastx/DoTheBackup
.. _virtualenv: https://virtualenv.pypa.io/
