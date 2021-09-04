"""unused import"""
# pylint: disable=undefined-all-variable, import-error, no-absolute-import
# pylint: disable=too-few-public-methods, missing-docstring
from __future__ import print_function  # noqa:F401
import xml.etree  # [unused-import]
import xml.sax  # noqa:F401  # [unused-import]
import os.path as test  # noqa:F401  # [unused-import]
from sys import argv as test2  # noqa:F401  # [unused-import]
from sys import flags  # noqa:F401  # [unused-import]
# +1:[unused-import,unused-import]
from collections import deque, OrderedDict, Counter  # noqa:F401
# All imports above should be ignored
import requests  # noqa:F401  # [unused-import]

# setuptools
import zipimport  # command/easy_install.py

# twisted
from importlib import invalidate_caches  # noqa:F401, E501  # python/test/test_deprecate.py

# astroid
import zipimport  # noqa:F401, F811  # manager.py
# IPython
from importlib.machinery import all_suffixes  # noqa:F401, E501  # core/completerlib.py
import importlib  # noqa:F401  # html/notebookapp.py

from IPython.utils.importstring import import_item  # noqa:F401  # Many files

# pyflakes
# test/test_doctests.py
from pyflakes.test.test_imports import Test as TestImports  # noqa:F401

# Nose
from nose.importer import Importer, add_path, remove_path  # loader.py

# see issue #88
import analytics
import flask_seasurf

import atexit
from __future__ import print_function
from docopt import docopt
import curses, logging, sqlite3
import logging
import os
import sqlite3
import time
import sys
import signal
import bs4
import nonexistendmodule
import boto as b, peewee as p
# import django
import flask.ext.somext  # noqa:F401  # # #
from sqlalchemy import model  # noqa:F401
try:
    import ujson as json
except ImportError:
    import json  # noqa:F401

import models  # noqa:F401


def main():
    pass


import after_method_is_valid_even_if_not_pep8  # noqa:F401, E402
