from __future__ import print_function
from distutils import spawn
from functools import wraps
import sys


def required_keys(key_list):
    '''Decorator to check against key list.
    '''
    def decorated_function(func):

        @wraps(func)
        def func_wrapper(config):
            for key in key_list:
                if key not in config.keys():
                    print('ERROR: "{}" not in config.'.format(key))
                    sys.exit()

            return func(config)
        return func_wrapper
    return decorated_function


def required_executables(dep_list):
    '''Decorator to check required executables.
    '''
    def decorated_function(func):

        @wraps(func)
        def func_wrapper(config):
            for dep in dep_list:
                if not spawn.find_executable(dep):
                    print('ERROR: Please install {}.'.format(dep))
                    sys.exit()

            return func(config)
        return func_wrapper
    return decorated_function
