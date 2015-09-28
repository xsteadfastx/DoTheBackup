import os


def inode_list(filelist):
    '''Returns a list of inodes for files.
    '''
    inodes = []
    for f in filelist:
        fd = os.open(f, os.O_RDONLY)
        info = os.fstat(fd)
        inodes.append(info.st_ino)

    return inodes
