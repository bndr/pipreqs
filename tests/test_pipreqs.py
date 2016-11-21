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
                        'peewee', 'ujson', 'nonexistendmodule', 'bs4', 'after_method_is_valid_even_if_not_pep8' ]
        self.modules2 = ['beautifulsoup4']
        self.local = ["docopt", "requests", "nose", 'pyflakes']
        self.project = os.path.join(os.path.dirname(__file__), "_data")
        self.project_invalid = os.path.join(os.path.dirname(__file__), "_invalid_data")
        self.project_with_ignore_directory = os.path.join(os.path.dirname(__file__), "_data_ignore")
        self.project_with_duplicated_deps = os.path.join(os.path.dirname(__file__), "_data_duplicated_deps")
        self.requirements_path = os.path.join(self.project, "requirements.txt")
        self.alt_requirement_path = os.path.join(
            self.project, "requirements2.txt")

    def test_get_all_imports(self):
        imports = pipreqs.get_all_imports(self.project)
        self.assertEqual(len(imports), 13)
        for item in imports:
            self.assertTrue(
                item.lower() in self.modules, "Import is missing: " + item)
        self.assertFalse("time" in imports)
        self.assertFalse("logging" in imports)
        self.assertFalse("curses" in imports)
        self.assertFalse("__future__" in imports)
        self.assertFalse("django" in imports)
        self.assertFalse("models" in imports)

    def test_deduplicate_dependencies(self):
        imports = pipreqs.get_all_imports(self.project_with_duplicated_deps)
        pkgs = pipreqs.get_pkg_names(imports)
        self.assertEqual(len(pkgs), 1)
        self.assertTrue("pymongo" in pkgs)

    def test_invalid_python(self):
        """
        Test that invalid python files cannot be imported.
        """
        self.assertRaises(SyntaxError, pipreqs.get_all_imports, self.project_invalid)

    def test_get_imports_info(self):
        """
        Test to see that the right number of packages were found on PyPI
        """
        imports = pipreqs.get_all_imports(self.project)
        with_info = pipreqs.get_imports_info(imports)
        # Should contain 10 items without the "nonexistendmodule" and "after_method_is_valid_even_if_not_pep8"
        self.assertEqual(len(with_info), 11)
        for item in with_info:
            self.assertTrue(
                item['name'].lower() in self.modules,
                "Import item appears to be missing " + item['name'])

    def test_get_use_local_only(self):
        """
        Test without checking PyPI, check to see if names of local imports matches what we expect

        - Note even though pyflakes isn't in requirements.txt,
          It's added to locals since it is a development dependency for testing
        """
        # should find only docopt and requests
        imports_with_info = pipreqs.get_import_local(self.modules)
        for item in imports_with_info:
            self.assertTrue(item['name'].lower() in self.local)

    def test_init(self):
        """
        Test that all modules we will test upon, are in requirements file
        """
        pipreqs.init({'<path>': self.project, '--savepath': None, '--print': False,
                      '--use-local': None, '--force': True, '--proxy':None, '--pypi-server':None})
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.read().lower()
            for item in self.modules[:-3]:
                self.assertTrue(item.lower() in data)

    def test_init_local_only(self):
        """
        Test that items listed in requirements.text are the same as locals expected
        """
        pipreqs.init({'<path>': self.project, '--savepath': None, '--print': False,
                      '--use-local': True, '--force': True, '--proxy':None, '--pypi-server':None})
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.readlines()
            for item in data:
                item = item.strip().split("==")
                self.assertTrue(item[0].lower() in self.local)

    def test_init_savepath(self):
        """
        Test that we can save requiremnts.tt correctly to a different path
        """
        pipreqs.init({'<path>': self.project, '--savepath':
                      self.alt_requirement_path, '--use-local': None, '--proxy':None, '--pypi-server':None,  '--print': False})
        assert os.path.exists(self.alt_requirement_path) == 1
        with open(self.alt_requirement_path, "r") as f:
            data = f.read().lower()
            for item in self.modules[:-3]:
                self.assertTrue(item.lower() in data)
            for item in self.modules2:
                self.assertTrue(item.lower() in data)

    def test_init_overwrite(self):
        """
        Test that if requiremnts.txt exists, it will not automatically be overwritten
        """
        with open(self.requirements_path, "w") as f:
            f.write("should_not_be_overwritten")
        pipreqs.init({'<path>': self.project, '--savepath': None,
                      '--use-local': None, '--force': None, '--proxy':None, '--pypi-server':None, '--print': False})
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.read().lower()
            self.assertEqual(data, "should_not_be_overwritten")

    def test_get_import_name_without_alias(self):
        """
        Test that function get_name_without_alias() will work on a string.
        - Note: This isn't truly needed when pipreqs is walking the AST to find imports
        """
        import_name_with_alias = "requests as R"
        expected_import_name_without_alias = "requests"
        import_name_without_aliases = pipreqs.get_name_without_alias(
            import_name_with_alias)
        self.assertEqual(
            import_name_without_aliases, expected_import_name_without_alias)

    def test_custom_pypi_server(self):
        """
        Test that trying to get a custom pypi sever fails correctly
        """
        self.assertRaises(requests.exceptions.MissingSchema, pipreqs.init, {'<path>': self.project, '--savepath': None, '--print': False,
                          '--use-local': None, '--force': True, '--proxy': None, '--pypi-server': 'nonexistent'})

    def test_ignored_directory(self):
        """
        Test --ignore parameter
        """
        pipreqs.init(
            {'<path>': self.project_with_ignore_directory, '--savepath': None, '--print': False,
                      '--use-local': None, '--force': True,
                      '--proxy':None,
                      '--pypi-server':None,
                      '--ignore':'.ignored_dir,.ignore_second'
            }
        )
        with open(os.path.join(self.project_with_ignore_directory, "requirements.txt"), "r") as f:
            data = f.read().lower()
            for item in ['click', 'getpass']:
                self.assertFalse(item.lower() in data)


    def tearDown(self):
        """
        Remove requiremnts.txt files that were written
        """
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
