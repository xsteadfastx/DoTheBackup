slapcat
=======

With this plugin you can backup LDAP-Databases. You can commit the changes to a git repository

Dependencies
------------

- **git**
- **slapcat**

Configuration
-------------

A list of required configuration keys:

- **destination**:
  The folder where the bacup is going to be saved to. Its just the name of the folder. The export itself will be called ``backup.ldif``.

Its also needed to define a ``mode``. Here is a list:

- **once**:
  This mode will run the ``slapcat`` command once and will overwrite a export that is already there.
- **git**:
  This mode will commit every change to the export after the export got created. This will save every change of it.

Here's a example::

   log_dir: /var/log/dothebackup
   backup:
     myldap:
       type: slapcat
       mode: git
       destination: /media/backup/myldap

Restore
-------

Example::

    slapadd -l /media/backup/myldap/backup.ldif
