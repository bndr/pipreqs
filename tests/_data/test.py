"""unused import"""
# pylint: disable=undefined-all-variable, import-error, no-absolute-import, too-few-public-methods, missing-docstring
import xml.etree  # [unused-import]
import xml.sax  # [unused-import]
import os.path as test  # [unused-import]
from sys import argv as test2  # [unused-import]
from sys import flags  # [unused-import]
# +1:[unused-import,unused-import]
from collections import deque, OrderedDict, Counter
# All imports above should be ignored
import requests  # [unused-import]

# setuptools
import zipimport  # command/easy_install.py

# twisted
from importlib import invalidate_caches  # python/test/test_deprecate.py

# astroid
import zipimport  # manager.py
# IPython
from importlib.machinery import all_suffixes  # core/completerlib.py
import importlib  # html/notebookapp.py

from IPython.utils.importstring import import_item  # Many files

# pyflakes
# test/test_doctests.py
from pyflakes.test.test_imports import Test as TestImports

# Nose
from nose.importer import Importer, add_path, remove_path  # loader.py

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
import boto as b, import peewee as p,
# import django
import flask.ext.somext  # # #
from sqlalchemy import model
try:
    import ujson as json
except ImportError:
    import json

import models


def main():
    pass

import after_method_should_be_ignored
