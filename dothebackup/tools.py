from datetime import datetime
import os


def absolutenormpath(path):
    '''Returns a absolute normalized path.'''
    return os.path.abspath(os.path.normpath(path))


def today():
    '''Returns todays day string.'''
    return datetime.utcnow().strftime('%d')
