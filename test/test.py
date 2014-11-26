import arrow
import unittest
import os
import yaml
import shutil
import tempfile
import mock
from DoTheBackup import from_file


class TestRsync(unittest.TestCase):
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
                        'backup/rsync-month-destination')},
                'test-rsync-once': {
                    'type': 'rsync_once',
                    'enabled': 'true',
                    'source': os.path.join(
                        test_dir,
                        'backup/rsync-once-source'),
                    'destination': os.path.join(
                        test_dir,
                        'backup/rsync-once-destination')}}}

    @staticmethod
    def inode_list(filelist):
        ''' returns a list of inodes for files '''
        inodes = []
        for f in filelist:
            fd = os.open(f, os.O_RDONLY)
            info = os.fstat(fd)
            inodes.append(info.st_ino)

        return inodes

    def setUp(self):
        # create some variables
        self.test_dir = tempfile.mkdtemp()

        self.now = arrow.utcnow()
        self.today = self.now.format('DD')
        self.yesterday = self.now.replace(days=-1).format('DD')

        # create config
        test_data = self.create_config(self.test_dir)

        # save yaml
        with open(os.path.join(self.test_dir, 'test.yaml'), 'w') as f:
            f.write(yaml.dump(test_data))

        # get config from test.yaml
        with open(os.path.join(self.test_dir, 'test.yaml')) as f:
            self.config = yaml.load(f)

        # create dirs and fake files
        os.makedirs(self.config['log_dir'])

        for scalar, sequence in self.config['backup'].items():
            os.makedirs(sequence['source'])
            for i in range(10):
                with tempfile.NamedTemporaryFile(mode='w',
                                                 dir=sequence['source']) as f:
                    f.write('THIS IS A TEST!')

            os.makedirs(sequence['destination'])

        self.arguments = {}
        self.arguments['<config>'] = os.path.join(self.test_dir, 'test.yaml')
        self.arguments['--verbose'] = False

        # run from_file to do the backup magic
        from_file(self.arguments)

    def tearDown(self):
        # delete test.yaml
        os.remove(os.path.join(
            self.test_dir,
            'test.yaml'))

        # delete tmp test folders
        shutil.rmtree(self.test_dir)

    def test_file_list(self):
        ''' source filelist is equal to destination filelist '''
        for scalar, sequence in self.config['backup'].items():
            source_filelist = os.listdir(sequence['source'])
            if sequence['type'] == 'rsync_month':
                destination_filelist = os.listdir(
                    os.path.join(sequence['destination'],
                                 self.today))
            else:
                destination_filelist = os.listdir(sequence['destination'])

            self.assertEqual(source_filelist, destination_filelist)

    def test_inodes(self):
        ''' inodes are the same if rsync_month is used '''
        for scalar, sequence in self.config['backup'].items():
            if sequence['type'] == 'rsync_month':
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

                self.assertEqual(today_inodes, yesterday_inodes)


class TestGitMySQL(unittest.TestCase):
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

    def setUp(self):
        # create some variables
        self.test_dir = tempfile.mkdtemp()

        # create config
        self.config_file = tempfile.mkstemp()[1]
        with open(self.config_file, 'w') as f:
            f.write(yaml.dump(self.create_config(self.test_dir)))

        # get config from test.yaml
        with open(self.config_file) as f:
            self.config = yaml.load(f)

        # create log dir
        os.makedirs(self.config['log_dir'])

        # set arguments
        self.arguments = {}
        self.arguments['<config>'] = self.config_file
        self.arguments['--verbose'] = False

    def tearDown(self):
        # remove temp files
        os.remove(self.config_file)
        shutil.rmtree(self.test_dir)

    @mock.patch('DoTheBackup.subprocess')
    def test_subprocess_called_with(self, subprocess):
        ''' subprocess arguments are as expected '''
        # mock stuff
        subprocess.Popen.return_value.returncode = 0

        # run DoTheBackup
        from_file(self.arguments)

        # testing if subprocess.Popen got called 4 times
        self.assertEqual(subprocess.Popen.call_count, 4)

        # getting subprocess calls
        calls = subprocess.Popen.call_args_list

        # list of awaited responses
        response_list = [
            str('mysqldump -umymysqluser '
                '-pmymysqlpassword '
                '--skip-extended-insert '
                'mydb > /destination/mydb.sql'),
            str('cd /destination && git add mydb.sql'),
            str('cd /destination && git commit -m "daily backup"'),
            str('cd /destination && git push remotebox master')]

        # checking every call argument with its awaited response
        for call, response in zip(calls, response_list):
            call_args, call_kwargs = call
            self.assertEqual(call_args[0], response)


if __name__ == '__main__':
    unittest.main()
