#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pipreqs
----------------------------------

Tests for `pipreqs` module.
"""

import unittest, os

from pipreqs import pipreqs


class TestPipreqs(unittest.TestCase):
    def setUp(self):
        self.modules = ['flask', 'requests', 'sqlalchemy', 'docopt', 'ujson', 'nonexistendmodule']
        self.project = os.path.join(os.path.dirname(__file__), "_data")
        self.requirements_path = os.path.join(self.project, "requirements.txt")

    def test_get_all_imports(self):
        imports = pipreqs.get_all_imports(self.project)
        self.assertEqual(len(imports), 6, "Incorrect Imports array length")
        for item in imports:
            self.assertTrue(item in self.modules, "Import is missing")
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
        self.assertEqual(len(with_info), 5, "Length of imports array with info is wrong")
        for item in with_info:
            self.assertTrue(item['name'] in self.modules, "Import item appears to be missing")
    
    def test_get_use_local_only(self):
    	# should find only docopt and requests
    	imports_with_info = pipreqs.get_import_local(self.modules)
    	self.assertTrue(len(imports_with_info) == 2)

    def test_init(self):
        pipreqs.init({'<path>': self.project, '--savepath': None,'--use-local':None})
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.read()
            for item in self.modules[:-1]:
                self.assertTrue(item in data)

    def tearDown(self):
        try:
            os.remove(self.requirements_path)
        except OSError:
            pass


if __name__ == '__main__':
    unittest.main()
