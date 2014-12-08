import arrow
import os
import yaml
import shutil
import tempfile
import mock
from DoTheBackup import from_file


class Helper(object):

    """Helper to setup tests.
    """

    @staticmethod
    def inode_list(filelist):
        """Returns a list of inodes for files.
        """
        inodes = []
        for f in filelist:
            fd = os.open(f, os.O_RDONLY)
            info = os.fstat(fd)
            inodes.append(info.st_ino)

        return inodes

    def setup_dothebackup(self):
        # create some variables
        self.now = arrow.utcnow()
        self.today = self.now.format('DD')
        self.yesterday = self.now.replace(days=-1).format('DD')
        self.test_dir = tempfile.mkdtemp()

        # create config
        test_config = self.create_config(self.test_dir)

        # save yaml
        with open(os.path.join(self.test_dir, 'test.yaml'), 'w') as f:
            f.write(yaml.dump(test_config))

        # get config from test.yaml
        with open(os.path.join(self.test_dir, 'test.yaml')) as f:
            self.config = yaml.load(f)

        # create logdir
        os.makedirs(self.config['log_dir'])

        # set arguments to serve docopt
        self.arguments = {}
        self.arguments['<config>'] = os.path.join(self.test_dir, 'test.yaml')
        self.arguments['--verbose'] = False

    def teardown_dothebackup(self):
        # delete test.yaml
        os.remove(os.path.join(
            self.test_dir,
            'test.yaml'))

        # delete tmp test folders
        shutil.rmtree(self.test_dir)

    def create_fake_data(self):
        """Creates test directories and test files.
        """
        # create dirs and fake files
        for scalar, sequence in self.config['backup'].items():
            os.makedirs(sequence['source'])
            for i in range(10):
                with tempfile.NamedTemporaryFile(mode='w',
                                                 dir=sequence['source']) as f:
                    f.write('THIS IS A TEST!')

            os.makedirs(sequence['destination'])


class TestRsyncMonth(Helper):

    @staticmethod
    def create_config(test_dir):
        return {
            'log_dir': os.path.join(
                test_dir,
                'logs'),
            'backup': {
                'test-rsync-month': {
                    'type': 'rsync_month',
                    'enabled': 'true',
                    'source': os.path.join(
                        test_dir,
                        'backup/rsync-month-source'),
                    'destination': os.path.join(
                        test_dir,
                        'backup/rsync-month-destination'),
                    'exclude': ['exclude_this', 'exclude_that'],
                    'include': ['include_this', 'include_that']}}}

    def setup_method(self, method):
        self.setup_dothebackup()
        self.create_fake_data()

    def teardown_method(self, method):
        self.teardown_dothebackup()

    def test_file_list(self):
        """Source filelist is equal to destination filelist.
        """
        # run DoTheBackup
        from_file(self.arguments)

        for scalar, sequence in self.config['backup'].items():
            source_filelist = os.listdir(sequence['source'])
            if sequence['type'] == 'rsync_month':
                destination_filelist = os.listdir(
                    os.path.join(sequence['destination'],
                                 self.today))
            else:
                destination_filelist = os.listdir(sequence['destination'])

            assert source_filelist == destination_filelist

    def test_inodes(self):
        """Inodes are the same if rsync_month is used.
        """
        # run DoTheBackup
        from_file(self.arguments)

        for scalar, sequence in self.config['backup'].items():
            destination = sequence['destination']

            # move the today dir to yesterday
            shutil.move(
                os.path.join(destination, self.today),
                os.path.join(destination, self.yesterday))

            # run from_file again
            from_file(self.arguments)

            # create inode list for the today backup dir
            today_dir = os.path.join(destination, self.today)
            today_filelist = [os.path.join(today_dir, f) for f
                              in os.listdir(today_dir)]
            today_inodes = self.inode_list(today_filelist)

            # create inode list for the yesterday backup dir
            yesterday_dir = os.path.join(destination, self.yesterday)
            yesterday_filelist = [os.path.join(yesterday_dir, f) for f
                                  in os.listdir(yesterday_dir)]
            yesterday_inodes = self.inode_list(yesterday_filelist)

            assert today_inodes == yesterday_inodes

    @mock.patch('DoTheBackup.subprocess')
    def test_subprocess_called_with(self, subprocess):
        """Subprocess arguments are as expected.
        """
        # mock stuff
        subprocess.Popen.return_value.returncode = 0

        # run DoTheBackup
        from_file(self.arguments)

        # testing if subprocess.Popen got called once
        assert subprocess.Popen.call_count == 1

        # getting subprocess calls
        calls = subprocess.Popen.call_args_list

        # list of awaited responses
        response_list = ['rsync -av --delete \
--exclude=exclude_this --exclude=exclude_that \
--include=include_this --include=include_that --link-dest=../{} \
{}/backup/rsync-month-source/ \
{}/backup/rsync-month-destination/{}'.format(self.yesterday,
                                             self.test_dir,
                                             self.test_dir,
                                             self.today)]

        # checking every call argument with its awaited response
        for call, response in zip(calls, response_list):
            call_args, call_kwargs = call

            assert call_args[0] == response


class TestRsyncOnce(Helper):

    @staticmethod
    def create_config(test_dir):
        return {
            'log_dir': os.path.join(
                test_dir,
                'logs'),
            'backup': {
                'test-rsync-once': {
                    'type': 'rsync_once',
                    'enabled': 'true',
                    'source': os.path.join(
                        test_dir,
                        'backup/rsync-once-source'),
                    'destination': os.path.join(
                        test_dir,
                        'backup/rsync-once-destination'),
                    'exclude': ['exclude_this', 'exclude_that'],
                    'include': ['include_this', 'include_that']}}}

    def setup_method(self, method):
        self.setup_dothebackup()
        self.create_fake_data()

    def teardown_method(self, method):
        self.teardown_dothebackup()

    def test_file_list(self):
        """Source filelist is equal to destination filelist.
        """
        # run DoTheBackup
        from_file(self.arguments)

        for scalar, sequence in self.config['backup'].items():
            source_filelist = os.listdir(sequence['source'])
            if sequence['type'] == 'rsync_month':
                destination_filelist = os.listdir(
                    os.path.join(sequence['destination'],
                                 self.today))
            else:
                destination_filelist = os.listdir(sequence['destination'])

            assert source_filelist == destination_filelist

    @mock.patch('DoTheBackup.subprocess')
    def test_subprocess_called_with(self, subprocess):
        """Subprocess arguments are as expected.
        """
        # mock stuff
        subprocess.Popen.return_value.returncode = 0

        # run DoTheBackup
        from_file(self.arguments)

        # testing if subprocess.Popen got called once
        assert subprocess.Popen.call_count == 1

        # getting subprocess calls
        calls = subprocess.Popen.call_args_list

        # list of awaited responses
        response_list = ['rsync -av --delete \
--exclude=exclude_this --exclude=exclude_that --include=include_this \
--include=include_that {}/backup/rsync-once-source/ \
{}/backup/rsync-once-destination'.format(self.test_dir,
                                         self.test_dir)]

        for call, response in zip(calls, response_list):
            call_args, call_kwargs = call
            assert call_args[0] == response


class TestGitMySQL(Helper):

    @staticmethod
    def create_config(test_dir):
        return {
            'log_dir': os.path.join(
                test_dir, 'logs'),
            'backup': {
                'test-git-mysql': {
                    'type': 'git_mysql',
                    'enabled': 'true',
                    'user': 'mymysqluser',
                    'password': 'mymysqlpassword',
                    'db_name': 'mydb',
                    'destination': '/destination',
                    'remote_name': 'remotebox'}}}

    def setup_method(self, method):
        self.setup_dothebackup()

    def teardown_method(self, method):
        self.teardown_dothebackup()

    @mock.patch('DoTheBackup.subprocess')
    def test_subprocess_called_with(self, subprocess):
        """Subprocess arguments are as expected.
        """
        # mock stuff
        subprocess.Popen.return_value.returncode = 0

        # run DoTheBackup
        from_file(self.arguments)

        # testing if subprocess.Popen got called 4 times
        assert subprocess.Popen.call_count == 4

        # getting subprocess calls
        calls = subprocess.Popen.call_args_list

        # list of awaited responses
        response_list = [
            ('mysqldump -umymysqluser '
             '-pmymysqlpassword '
             '--skip-extended-insert '
             'mydb > /destination/mydb.sql'),
            ('cd /destination && git add mydb.sql'),
            ('cd /destination && git commit -m "daily backup"'),
            ('cd /destination && git push remotebox master')]

        # checking every call argument with its awaited response
        for call, response in zip(calls, response_list):
            call_args, call_kwargs = call
            assert call_args[0] == response
