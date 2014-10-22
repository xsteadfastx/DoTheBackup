import arrow
import unittest
import os
import yaml
import shutil
from uuid import uuid4
from DoTheBackup import from_file


def inode_list(filelist):
    inodes = []
    for f in filelist:
        fd = os.open(f, os.O_RDONLY)
        info = os.fstat(fd)
        inodes.append(info.st_ino)

    return inodes


class TestDoTheBackup(unittest.TestCase):
    def setUp(self):
        # create some time variables
        self.now = arrow.utcnow()
        self.today = self.now.format('DD')
        self.yesterday = self.now.replace(days=-1).format('DD')

        # get config from test.yaml
        with open('test.yaml') as f:
            self.config = yaml.load(f)

        # create dirs and fake files
        os.makedirs(self.config['log_dir'])

        for scalar, sequence in self.config['backup'].viewitems():
            os.makedirs(sequence['source'])
            for i in range(10):
                uuid = str(uuid4())
                with open(os.path.join(sequence['source'], uuid),
                          'w') as f:
                    f.write(uuid)

            os.makedirs(sequence['destination'])

        self.arguments = {}
        self.arguments['<config>'] = 'test.yaml'
        self.arguments['--verbose'] = False

        # run from_file to do the backup magic
        from_file(self.arguments)

    def tearDown(self):
        # delete tmp test folders
        shutil.rmtree('tmp-test')

    def test_file_list(self):
        ''' test if source filelist is equal to destination filelist '''
        for scalar, sequence in self.config['backup'].viewitems():
            source_filelist = os.listdir(sequence['source'])
            if sequence['type'] == 'rsync_month':
                destination_filelist = os.listdir(
                    os.path.join(sequence['destination'],
                                 self.today))
            else:
                destination_filelist = os.listdir(sequence['destination'])

            self.assertEqual(source_filelist, destination_filelist)

    def test_inodes(self):
        ''' check if the inodes are the same if rsync_month is used '''
        for scalar, sequence in self.config['backup'].viewitems():
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
                today_filelist = [os.path.join(today_dir, f) for f in os.listdir(today_dir)]
                today_inodes = inode_list(today_filelist)

                # create inode list for the yesterday backup dir
                yesterday_dir = os.path.join(destination, self.yesterday)
                yesterday_filelist = [os.path.join(yesterday_dir, f) for f in os.listdir(yesterday_dir)]
                yesterday_inodes = inode_list(yesterday_filelist)

                self.assertEqual(today_inodes, yesterday_inodes)

    def test_exit_codes(self):
        pass


if __name__ == '__main__':
    unittest.main()
