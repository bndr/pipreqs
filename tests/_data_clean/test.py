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
from nose.importer import Importer, add_path, remove_path  # noqa:F401, E501  # loader.py

# see issue #88
import analytics  # noqa:F401
import flask_seasurf  # noqa:F401

import atexit  # noqa:F401
from docopt import docopt  # noqa:F401
import curses, logging, sqlite3  # noqa:F401, E401
import logging  # noqa:F401, F811
import os  # noqa:F401
import sqlite3  # noqa:F401, F811
import time  # noqa:F401
import sys  # noqa:F401
import signal  # noqa:F401
import bs4  # noqa:F401
import nonexistendmodule  # noqa:F401
import boto as b, peewee as p  # noqa:F401, E401
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
