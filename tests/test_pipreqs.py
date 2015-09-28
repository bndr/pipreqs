#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pipreqs
----------------------------------

Tests for `pipreqs` module.
"""

import unittest
import os
import requests

from pipreqs import pipreqs


class TestPipreqs(unittest.TestCase):

    def setUp(self):
        self.modules = ['flask', 'requests', 'sqlalchemy',
                        'docopt', 'boto', 'ipython', 'pyflakes', 'nose',
                        'peewee', 'ujson', 'nonexistendmodule', 'bs4', ]
        self.modules2 = ['beautifulsoup4']
        self.local = ["docopt", "requests", "nose"]
        self.project = os.path.join(os.path.dirname(__file__), "_data")
        self.requirements_path = os.path.join(self.project, "requirements.txt")
        self.alt_requirement_path = os.path.join(
            self.project, "requirements2.txt")

    def test_get_all_imports(self):
        imports = pipreqs.get_all_imports(self.project)
        self.assertEqual(len(imports), 12)
        for item in imports:
            self.assertTrue(
                item.lower() in self.modules, "Import is missing: " + item)
        self.assertFalse("time" in imports)
        self.assertFalse("logging" in imports)
        self.assertFalse("curses" in imports)
        self.assertFalse("__future__" in imports)
        self.assertFalse("django" in imports)
        self.assertFalse("models" in imports)

    def test_get_imports_info(self):
        imports = pipreqs.get_all_imports(self.project)
        with_info = pipreqs.get_imports_info(imports)
        # Should contain only 5 Elements without the "nonexistendmodule"
        self.assertEqual(len(with_info), 10)
        for item in with_info:
            self.assertTrue(
                item['name'].lower() in self.modules,
                "Import item appears to be missing " + item['name'])

    def test_get_use_local_only(self):
        # should find only docopt and requests
        imports_with_info = pipreqs.get_import_local(self.modules)
        for item in imports_with_info:
            self.assertTrue(item['name'].lower() in self.local)

    def test_init(self):
        pipreqs.init({'<path>': self.project, '--savepath': None,
                      '--use-local': None, '--force': True, '--proxy':None, '--pypi-server':None})
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.read().lower()
            for item in self.modules[:-2]:
                self.assertTrue(item.lower() in data)

    def test_init_local_only(self):
        pipreqs.init({'<path>': self.project, '--savepath': None,
                      '--use-local': True, '--force': True, '--proxy':None, '--pypi-server':None})
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.readlines()
            for item in data:
                item = item.strip().split(" == ")
                self.assertTrue(item[0].lower() in self.local)

    def test_init_savepath(self):
        pipreqs.init({'<path>': self.project, '--savepath':
                      self.alt_requirement_path, '--use-local': None, '--proxy':None, '--pypi-server':None})
        assert os.path.exists(self.alt_requirement_path) == 1
        with open(self.alt_requirement_path, "r") as f:
            data = f.read().lower()
            for item in self.modules[:-2]:
                self.assertTrue(item.lower() in data)
            for item in self.modules2:
                self.assertTrue(item.lower() in data)

    def test_init_overwrite(self):
        with open(self.requirements_path, "w") as f:
            f.write("should_not_be_overwritten")
        pipreqs.init({'<path>': self.project, '--savepath': None,
                      '--use-local': None, '--force': None, '--proxy':None, '--pypi-server':None})
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.read().lower()
            self.assertEqual(data, "should_not_be_overwritten")

    def test_get_import_name_without_alias(self):
        import_name_with_alias = "requests as R"
        expected_import_name_without_alias = "requests"
        import_name_without_aliases = pipreqs.get_name_without_alias(
            import_name_with_alias)
        self.assertEqual(
            import_name_without_aliases, expected_import_name_without_alias)


    def test_custom_pypi_server(self):
        with self.assertRaises(requests.exceptions.MissingSchema):
            pipreqs.init({'<path>': self.project, '--savepath': None,
                      '--use-local': None, '--force': True, '--proxy':None, '--pypi-server':'nonexistent'})


    def tearDown(self):
        try:
            os.remove(self.requirements_path)
        except OSError:
            pass
        try:
            os.remove(self.alt_requirement_path)
        except OSError:
            pass


if __name__ == '__main__':
    unittest.main()
