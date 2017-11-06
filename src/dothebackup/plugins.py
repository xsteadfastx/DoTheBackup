"""Plugins."""

import logging
import os
import sys
from distutils import spawn  # pylint: disable=no-name-in-module
from functools import wraps
from typing import Callable, Dict, List, Union

from dothebackup.types import CONFIGTYPE

LOG = logging.getLogger(__name__)


def load_plugins() -> Dict[str, Callable]:
    """Load plugins from plugin directory.

    This function reads the plugs directory and loads all plugins.
    """
    plugins = {}
    path = os.path.dirname(os.path.realpath(__file__)) + '/plugs'

    # temp extend sys path
    sys.path.insert(0, path)

    for file in os.listdir(path):
        fname, ext = os.path.splitext(file)
        if ext == '.py':
            mod = __import__(fname)
            plugins[fname] = mod.main
            LOG.debug('added %s plugin', fname)

    # remove temp sys path
    sys.path.pop(0)

    return plugins


def required_keys(key_list: List[str]) -> Callable:
    """Decorator to check against key list.

    :param key_list: List of keys that needs to be in the config
    :returns: Decorated function
    """
    # pylint: disable=missing-docstring
    def decorated_function(func: Callable) -> Callable:

        @wraps(func)
        def func_wrapper(config: CONFIGTYPE) -> Union[Callable, None]:
            for key in key_list:
                if key not in config.keys():
                    print('ERROR: "{}" not in config.'.format(key))
                    sys.exit(1)

            return func(config)

        return func_wrapper

    return decorated_function


def required_executables(dep_list: List[str]) -> Callable:
    """Decorator to check required executables.

    :param dep_list: Dependency list
    :returns: Decorated function
    """
    # pylint: disable=missing-docstring
    def decorated_function(func: Callable) -> Callable:

        @wraps(func)
        def func_wrapper(config: CONFIGTYPE) -> Union[Callable, None]:
            for dep in dep_list:
                if not spawn.find_executable(dep):
                    print('ERROR: Please install {}.'.format(dep))
                    sys.exit(1)

            return func(config)

        return func_wrapper

    return decorated_function
