import logging
import os
import sys

from distutils import spawn
from functools import wraps

log = logging.getLogger(__name__)


def load_plugins():
    """Load plugins from plugin directory.

    This function reads the plugs directory and loads all plugins.
    """
    plugins = {}
    path = os.path.dirname(os.path.realpath(__file__)) + '/plugs'

    # temp extend sys path
    sys.path.insert(0, path)

    for f in os.listdir(path):
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            mod = __import__(fname)
            plugins[fname] = mod.main
            log.debug('added {} plugin'.format(fname))

    # remove temp sys path
    sys.path.pop(0)

    return plugins


def required_keys(key_list):
    """Decorator to check against key list.

    :param key_list: List of keys that needs to be in the config
    :type key_list: list
    :returns: Decorated function
    :rtype: function
    """
    def decorated_function(func):

        @wraps(func)
        def func_wrapper(config):
            for key in key_list:
                if key not in config.keys():
                    print('ERROR: "{}" not in config.'.format(key))
                    sys.exit(1)

            return func(config)

        return func_wrapper

    return decorated_function


def required_executables(dep_list):
    """Decorator to check required executables.

    :param dep_list: Dependency list
    :type dep_list: list
    :returns: Decorated function
    :rtype: function
    """
    def decorated_function(func):

        @wraps(func)
        def func_wrapper(config):
            for dep in dep_list:
                if not spawn.find_executable(dep):
                    print('ERROR: Please install {}.'.format(dep))
                    sys.exit(1)

            return func(config)

        return func_wrapper

    return decorated_function
