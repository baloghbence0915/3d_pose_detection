from os.path import join
import os

def getAbsolutePath(__file, *paths):
    cwd = os.path.dirname(os.path.realpath(__file))
    return join(cwd, *paths)
