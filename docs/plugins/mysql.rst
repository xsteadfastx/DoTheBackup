mysql
=====

With this plugin you can backup MySQL-Databases. You also can commit the changes to a git repository.

Dependencies
------------

- **git**
- **mysqldump**

Configuration
-------------

A list of required configuration keys:

- **server**:
  The hostname or ip of the MySQL server.
- **username**:
  A username that is allowed to login and backup stuff. The recommended way is to create a special backup user. Consider `Create MySQL BACKUPUSER`_.
- **password**:
  Password for the MySQL user.
- **database**:
  Name of the database to backup.
- **destination**:
  The folder where the backup is going to be saved to. Its just the name of the folder. The dump itself will be called ``<databasename>.sql``.

Its also needed to define a ``mode``. Here is a list:

- **once**:
  This mode will run the ``mysqldump`` command once and will overwrite a dump that is already there.
- **git**:
  This mode will commit every change to the dump after the dump got created. This will save every change of it. For a large database with alot of changes this can be a little heavy. But for small database this may be the best solution.

Here's an example::

    log_dir: /var/log/dothebackup
    backup:
      mydatabase:
        enabled: yes
        type: mysql
        mode: git
        server: localhost
        username: backupuser
        password: backuppassword
        database: mydatabase
        destination: /media/backup/mydatabase

Create MySQL BACKUPUSER
------------------------

If you want to create a user that can backup all databases::

    # /usr/bin/mysql -uroot -p
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or g.
    Your MySQL connection id is 253404
    Server version: 5.1.54-1ubuntu4 (Ubuntu)

    Copyright (c) 2000, 2010, Oracle and/or its affiliates. All rights reserved.
    This software comes with ABSOLUTELY NO WARRANTY. This is free software,
    and you are welcome to modify and redistribute it under the GPL v2 license

    Type 'help;' or 'h' for help. Type 'c' to clear the current input statement.

    mysql> GRANT LOCK TABLES, SELECT ON *.* TO 'BACKUPUSER'@'%' IDENTIFIED BY 'PASSWORD';
    Query OK, 0 rows affected (0.01 sec)

    mysql> flush privileges;
    Query OK, 0 rows affected (0.00 sec)

    mysql> Bye

If you only want the BACKUPUSER to have permissions to one database, you can modify the command::

    GRANT LOCK TABLES, SELECT ON DATABASE.* TO 'BACKUPUSER'@'%' IDENTIFIED BY 'PASSWORD';

Thanks to `Ben Cane`_ for that information.

.. _Ben Cane: http://bencane.com/2011/12/12/creating-a-read-only-backup-user-for-mysqldump/
