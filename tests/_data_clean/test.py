"""unused import"""
# pylint: disable=undefined-all-variable, import-error, no-absolute-import, too-few-public-methods, missing-docstring
from __future__ import print_function

import atexit
import curses
import importlib  # html/notebookapp.py
import logging
import os
import os.path as test  # [unused-import]
import signal
import sqlite3
import sys
import time
import xml.etree  # [unused-import]
import xml.sax  # [unused-import]
# astroid
# setuptools
import zipimport  # manager.py
# +1:[unused-import,unused-import]
from collections import Counter, OrderedDict, deque
# twisted
from importlib import invalidate_caches  # python/test/test_deprecate.py
# IPython
from importlib.machinery import all_suffixes  # core/completerlib.py
from sys import argv as test2  # [unused-import]
from sys import flags  # [unused-import]

# see issue #88
import analytics
import boto as b
import bs4
# import django
import flask.ext.somext  # # #
import flask_seasurf
import nonexistendmodule
import peewee as p
# All imports above should be ignored
import requests  # [unused-import]
from docopt import docopt
from IPython.utils.importstring import import_item  # Many files
# Nose
from nose.importer import Importer, add_path, remove_path  # loader.py
# pyflakes
# test/test_doctests.py
from pyflakes.test.test_imports import Test as TestImports

# from sqlalchemy import model
try:
    import ujson as json
except ImportError:
    import json

import models


def main():
    pass


import after_method_is_valid_even_if_not_pep8
