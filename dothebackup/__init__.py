import os
import sys

# PLUGIN LOADER
# -------------

# dict to store the plugins by its name as key
PLUGINS = {}

path = os.path.dirname(os.path.realpath(__file__)) + '/plugs'

# temp extend sys path
sys.path.insert(0, path)

for f in os.listdir(path):
    fname, ext = os.path.splitext(f)
    if ext == '.py':
        mod = __import__(fname)
        PLUGINS[fname] = mod.main

# remove temp sys path
sys.path.pop(0)
