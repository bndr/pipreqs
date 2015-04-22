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
    	self.modules = ['flask', 'requests', 'sqlalchemy', 'docopt']

    def test_get_all_imports(self):
    	path = os.path.join(os.path.dirname(__file__),"_data")
    	imports = pipreqs.get_all_imports(path)
    	self.assertEqual(len(imports),4, "Incorrect Imports array length")
    	for item in imports:
    		self.assertTrue(item in self.modules, "Import is missing")

    def test_get_imports_info(self):
    	path = os.path.join(os.path.dirname(__file__),"_data")
    	imports = pipreqs.get_all_imports(path)
    	with_info = pipreqs.get_imports_info(imports)
    	self.assertEqual(len(with_info),4, "Length of imports array with info is wrong")
    	for item in with_info:
    		self.assertTrue(item['name'] in self.modules, "Import item appears to be missing")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
