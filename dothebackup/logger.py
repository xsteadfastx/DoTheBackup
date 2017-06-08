import logging

import os

from contextlib import contextmanager

from typing import IO, Iterator, List


debuglog = logging.getLogger(__name__)


class Logger(object):
    """A logger for handling stdout logging.

    :param log_dir: Directory to store logfiles in
    :param name: Name of the backup job
    :param keep: Number of logs to keep
    """
    def __init__(self, log_dir: str, name: str, keep: int) -> None:
        self.log_dir = log_dir
        self.name = name
        self.keep = keep

    def _old_logs(self) -> List[str]:
        """Create a list of old logfiles.

        :returns: A list of old logfiles
        :rtype: list
        """
        logs = [log
                for log in os.listdir(os.path.abspath(self.log_dir))
                if log.startswith(self.name)]

        return list(reversed(sorted(logs)))

    def rotate(self) -> None:
        """A logfile rotator.

        This function moves old logfiles around.

        Example::

            foo.log

        gets::

            foo.log.0001

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
                name, extension, log_number = log.split('.')

                number = int(log_number)

                os.rename(
                    os.path.join(
                        self.log_dir,
                        log
                    ),
                    os.path.join(
                        self.log_dir,
                        '{name}.log.{number:04d}'.format(
                            name=self.name,
                            number=number + 1
                        )
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
                            '{}.log.0001'.format(self.name)
                        )
                    )

    @contextmanager
    def logfile(self) -> Iterator[IO[str]]:
        """A logfile handler.

        This is used in a context to write to a logfile::

            with logger.logfile() as logfile:
                logfile.write('foobar')

        :yields: Opened logfile
        """
        f = open('{}.log'.format(os.path.join(self.log_dir, self.name)), 'a')

        yield f

        f.close()

    def create_log_dir(self) -> None:
        """Create logdir if its not there.
        """
        debuglog.debug('log_dir: {}'.format(self.log_dir))

        if not os.path.exists(self.log_dir):
            debuglog.debug('create: {}'.format(self.log_dir))
            os.makedirs(self.log_dir)
