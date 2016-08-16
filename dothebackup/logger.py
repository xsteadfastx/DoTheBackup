import attr
import logging
import os

from contextlib import contextmanager


debuglog = logging.getLogger(__name__)


@attr.s
class Logger(object):
    """A logger for handling stdout logging.

    :param log_dir: Directory to store logfiles in
    :param name: Name of the backup job
    :param keep: Number of logs to keep
    :type log_dir: str
    :type name: str
    :type keep: int
    """
    log_dir = attr.ib()
    name = attr.ib()
    keep = attr.ib()

    def _old_logs(self):
        """Create a list of old logfiles.

        :returns: A list of old logfiles
        :rtype: list
        """
        logs = [log
                for log in os.listdir(os.path.abspath(self.log_dir))
                if log.startswith(self.name)]

        return list(reversed(sorted(logs)))

    def rotate(self):
        """A logfile rotator.

        This function moves old logfiles around.

        Example::

            foo.log

        gets::

            foo.log.1

        and so on.
        """
        old_logs = self._old_logs()

        # remove last log if it came to the end of logs to keep
        if old_logs:
            if len(old_logs[0].split('.')) == 3 and \
                    int(old_logs[0].split('.')[-1]) == self.keep:

                # delete log
                os.remove(os.path.join(self.log_dir, old_logs[0]))

                # remove from old_logs list
                del old_logs[0]

        # iterate over the other old logs
        for log in old_logs:

            if len(log.split('.')) == 3:
                name, extension, number = log.split('.')

                number = int(number)

                os.rename(
                    os.path.join(
                        self.log_dir,
                        log
                    ),
                    os.path.join(
                        self.log_dir,
                        '{}.log.{}'.format(self.name, number + 1)
                    )
                )

            else:
                # if its the second log
                if len(log.split('.')) == 2:
                    os.rename(
                        os.path.join(
                            self.log_dir,
                            log
                        ),
                        os.path.join(
                            self.log_dir,
                            '{}.log.1'.format(self.name)
                        )
                    )

    @contextmanager
    def logfile(self):
        """A logfile handler.

        This is used in a context to write to a logfile::

            with logger.logfile() as logfile:
                logfile.write('foobar')

        :yields: Opened logfile
        :Yield type: _io.TextIOWrapper
        """
        # if log_dir does not exists, create it
        debuglog.debug('log_dir: {}'.format(self.log_dir))

        if not os.path.exists(self.log_dir):
            debuglog.debug('create: {}'.format(self.log_dir))
            os.makedirs(self.log_dir)

        f = open('{}.log'.format(os.path.join(self.log_dir, self.name)), 'a')

        yield f

        f.close()
