#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pipreqs
----------------------------------

Tests for `pipreqs` module.
"""

from io import StringIO
import logging
from unittest.mock import patch, Mock
import unittest
import os
import requests
import sys
import warnings

from pipreqs import pipreqs


class TestPipreqs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Disable all logs for not spamming the terminal when running tests.
        logging.disable(logging.CRITICAL)

        # Specific warning not covered by the above command:
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="jupyter_client")

        cls.modules = [
            "flask",
            "requests",
            "sqlalchemy",
            "docopt",
            "boto",
            "ipython",
            "pyflakes",
            "nose",
            "analytics",
            "flask_seasurf",
            "peewee",
            "ujson",
            "nonexistendmodule",
            "bs4",
            "after_method_is_valid_even_if_not_pep8",
        ]
        cls.modules2 = ["beautifulsoup4"]
        cls.local = ["docopt", "requests", "nose", "pyflakes", "ipython"]
        cls.project = os.path.join(os.path.dirname(__file__), "_data")
        cls.empty_filepath = os.path.join(cls.project, "empty.txt")
        cls.imports_filepath = os.path.join(cls.project, "imports.txt")
        cls.imports_no_version_filepath = os.path.join(cls.project, "imports_no_version.txt")
        cls.imports_any_version_filepath = os.path.join(cls.project, "imports_any_version.txt")
        cls.non_existent_filepath = os.path.join(cls.project, "non_existent_file.txt")

        cls.parsed_packages = [
            {"name": "pandas", "version": "2.0.0"},
            {"name": "numpy", "version": "1.2.3"},
            {"name": "torch", "version": "4.0.0"},
        ]

        cls.parsed_packages_no_version = [
            {"name": "pandas", "version": None},
            {"name": "tensorflow", "version": None},
            {"name": "torch", "version": None},
        ]

        cls.parsed_packages_any_version = [
            {"name": "numpy", "version": None},
            {"name": "pandas", "version": "2.0.0"},
            {"name": "tensorflow", "version": None},
            {"name": "torch", "version": "4.0.0"},
        ]

        cls.project_clean = os.path.join(os.path.dirname(__file__), "_data_clean")
        cls.project_invalid = os.path.join(os.path.dirname(__file__), "_invalid_data")
        cls.project_with_ignore_directory = os.path.join(os.path.dirname(__file__), "_data_ignore")
        cls.project_with_duplicated_deps = os.path.join(os.path.dirname(__file__), "_data_duplicated_deps")

        cls.requirements_path = os.path.join(cls.project, "requirements.txt")
        cls.alt_requirement_path = os.path.join(cls.project, "requirements2.txt")
        cls.non_existing_filepath = "xpto"

        cls.project_with_notebooks = os.path.join(os.path.dirname(__file__), "_data_notebook")
        cls.project_with_invalid_notebooks = os.path.join(os.path.dirname(__file__), "_invalid_data_notebook")

        cls.python_path_same_imports = os.path.join(os.path.dirname(__file__), "_data/test.py")
        cls.notebook_path_same_imports = os.path.join(os.path.dirname(__file__), "_data_notebook/test.ipynb")

    def test_get_all_imports(self):
        imports = pipreqs.get_all_imports(self.project)
        self.assertEqual(len(imports), 15)
        for item in imports:
            self.assertTrue(item.lower() in self.modules, "Import is missing: " + item)
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
        # Should contain 10 items without the "nonexistendmodule" and
        # "after_method_is_valid_even_if_not_pep8"
        self.assertEqual(len(with_info), 13)
        for item in with_info:
            self.assertTrue(
                item["name"].lower() in self.modules,
                "Import item appears to be missing " + item["name"],
            )

    def test_get_pkg_names(self):
        pkgs = ["jury", "Japan", "camel", "Caroline"]
        actual_output = pipreqs.get_pkg_names(pkgs)
        expected_output = ["camel", "Caroline", "Japan", "jury"]
        self.assertEqual(actual_output, expected_output)

    def test_get_use_local_only(self):
        """
        Test without checking PyPI, check to see if names of local
        imports matches what we expect

        - Note even though pyflakes isn't in requirements.txt,
          It's added to locals since it is a development dependency
          for testing
        """
        # should find only docopt and requests
        imports_with_info = pipreqs.get_import_local(self.modules)
        for item in imports_with_info:
            self.assertTrue(item["name"].lower() in self.local)

    @patch("pipreqs.pipreqs.get_locally_installed_packages")
    def test_get_import_local_only_from_venv(self, mock_get_local_packages):
        mock_get_local_packages.return_value = [
            {"name": "requests", "version": "2.31.0", "exports": ["requests"]},
            {"name": "docopt", "version": "0.6.2", "exports": ["docopt"]},
        ]

        imports = {"requests": "2.31.0", "docopt": "0.6.2", "flask": "3.0.2"}

        result = pipreqs.get_import_local(imports, use_venv_packages=True)

        self.assertEqual(result, [
            {"name": "requests", "version": "2.31.0", "exports": ["requests"]},
            {"name": "docopt", "version": "0.6.2", "exports": ["docopt"]},
        ])

    def test_init(self):
        """
        Test that all modules we will test upon are in requirements file
        """
        pipreqs.init(
            {
                "<path>": self.project,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.read().lower()
            for item in self.modules[:-3]:
                self.assertTrue(item.lower() in data)
        # It should be sorted based on names.
        data = data.strip().split("\n")
        self.assertEqual(data, sorted(data))

    def test_init_local_only(self):
        """
        Test that items listed in requirements.text are the same
        as locals expected
        """
        pipreqs.init(
            {
                "<path>": self.project,
                "--savepath": None,
                "--print": False,
                "--use-local": True,
                "--only-venv": False,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.readlines()
            for item in data:
                item = item.strip().split("==")
                self.assertTrue(item[0].lower() in self.local)

    def test_init_savepath(self):
        """
        Test that we can save requirements.txt correctly
        to a different path
        """
        pipreqs.init(
            {
                "<path>": self.project,
                "--savepath": self.alt_requirement_path,
                "--use-local": None,
                "--proxy": None,
                "--pypi-server": None,
                "--print": False,
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )
        assert os.path.exists(self.alt_requirement_path) == 1
        with open(self.alt_requirement_path, "r") as f:
            data = f.read().lower()
            for item in self.modules[:-3]:
                self.assertTrue(item.lower() in data)
            for item in self.modules2:
                self.assertTrue(item.lower() in data)

    def test_init_overwrite(self):
        """
        Test that if requiremnts.txt exists, it will not be
        automatically overwritten
        """
        with open(self.requirements_path, "w") as f:
            f.write("should_not_be_overwritten")
        pipreqs.init(
            {
                "<path>": self.project,
                "--savepath": None,
                "--use-local": None,
                "--force": None,
                "--proxy": None,
                "--pypi-server": None,
                "--print": False,
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )
        assert os.path.exists(self.requirements_path) == 1
        with open(self.requirements_path, "r") as f:
            data = f.read().lower()
            self.assertEqual(data, "should_not_be_overwritten")

    def test_get_import_name_without_alias(self):
        """
        Test that function get_name_without_alias()
        will work on a string.
        - Note: This isn't truly needed when pipreqs is walking
          the AST to find imports
        """
        import_name_with_alias = "requests as R"
        expected_import_name_without_alias = "requests"
        import_name_without_aliases = pipreqs.get_name_without_alias(import_name_with_alias)
        self.assertEqual(import_name_without_aliases, expected_import_name_without_alias)

    def test_custom_pypi_server(self):
        """
        Test that trying to get a custom pypi sever fails correctly
        """
        self.assertRaises(
            requests.exceptions.MissingSchema,
            pipreqs.init,
            {
                "<path>": self.project,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": "nonexistent",
            },
        )

    def test_ignored_directory(self):
        """
        Test --ignore parameter
        """
        pipreqs.init(
            {
                "<path>": self.project_with_ignore_directory,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--ignore": ".ignored_dir,.ignore_second",
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )
        with open(os.path.join(self.project_with_ignore_directory, "requirements.txt"), "r") as f:
            data = f.read().lower()
            for item in ["click", "getpass"]:
                self.assertFalse(item.lower() in data)

    def test_dynamic_version_no_pin_scheme(self):
        """
        Test --mode=no-pin
        """
        pipreqs.init(
            {
                "<path>": self.project_with_ignore_directory,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": "no-pin",
            }
        )
        with open(os.path.join(self.project_with_ignore_directory, "requirements.txt"), "r") as f:
            data = f.read().lower()
            for item in ["beautifulsoup4", "boto"]:
                self.assertTrue(item.lower() in data)

    def test_dynamic_version_gt_scheme(self):
        """
        Test --mode=gt
        """
        pipreqs.init(
            {
                "<path>": self.project_with_ignore_directory,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": "gt",
            }
        )
        with open(os.path.join(self.project_with_ignore_directory, "requirements.txt"), "r") as f:
            data = f.readlines()
            for item in data:
                symbol = ">="
                message = "symbol is not in item"
                self.assertIn(symbol, item, message)

    def test_dynamic_version_compat_scheme(self):
        """
        Test --mode=compat
        """
        pipreqs.init(
            {
                "<path>": self.project_with_ignore_directory,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": "compat",
            }
        )
        with open(os.path.join(self.project_with_ignore_directory, "requirements.txt"), "r") as f:
            data = f.readlines()
            for item in data:
                symbol = "~="
                message = "symbol is not in item"
                self.assertIn(symbol, item, message)

    def test_clean(self):
        """
        Test --clean parameter
        """
        pipreqs.init(
            {
                "<path>": self.project,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )
        assert os.path.exists(self.requirements_path) == 1
        pipreqs.init(
            {
                "<path>": self.project,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": None,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": self.requirements_path,
                "--mode": "non-pin",
            }
        )
        with open(self.requirements_path, "r") as f:
            data = f.read().lower()
            for item in self.modules[:-3]:
                self.assertTrue(item.lower() in data)

    def test_clean_with_imports_to_clean(self):
        """
        Test --clean parameter when there are imports to clean
        """
        cleaned_module = "sqlalchemy"
        pipreqs.init(
            {
                "<path>": self.project,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )
        assert os.path.exists(self.requirements_path) == 1
        pipreqs.init(
            {
                "<path>": self.project_clean,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": None,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": self.requirements_path,
                "--mode": "non-pin",
            }
        )
        with open(self.requirements_path, "r") as f:
            data = f.read().lower()
            self.assertTrue(cleaned_module not in data)

    def test_compare_modules(self):
        test_cases = [
            (self.empty_filepath, [], set()),  # both empty
            (self.empty_filepath, self.parsed_packages, set()),  # only file empty
            (
                self.imports_filepath,
                [],
                set(package["name"] for package in self.parsed_packages),
            ),  # only imports empty
            (self.imports_filepath, self.parsed_packages, set()),  # no difference
            (
                self.imports_filepath,
                self.parsed_packages[1:],
                set([self.parsed_packages[0]["name"]]),
            ),  # common case
        ]

        for test_case in test_cases:
            with self.subTest(test_case):
                filename, imports, expected_modules_not_imported = test_case

                modules_not_imported = pipreqs.compare_modules(filename, imports)

                self.assertSetEqual(modules_not_imported, expected_modules_not_imported)

    def test_output_requirements(self):
        """
        Test --print parameter
        It should print to stdout the same content as requeriments.txt
        """

        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        pipreqs.init(
            {
                "<path>": self.project,
                "--savepath": None,
                "--print": True,
                "--use-local": None,
                "--force": None,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )
        pipreqs.init(
            {
                "<path>": self.project,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )

        with open(self.requirements_path, "r") as f:
            file_content = f.read().lower()
            stdout_content = capturedOutput.getvalue().lower()
            self.assertTrue(file_content == stdout_content)

    def test_import_notebooks(self):
        """
        Test the function get_all_imports() using .ipynb file
        """
        self.mock_scan_notebooks()
        imports = pipreqs.get_all_imports(self.project_with_notebooks)
        for item in imports:
            self.assertTrue(item.lower() in self.modules, "Import is missing: " + item)
        not_desired_imports = ["time", "logging", "curses", "__future__", "django", "models", "FastAPI", "sklearn"]
        for not_desired_import in not_desired_imports:
            self.assertFalse(
                not_desired_import in imports,
                f"{not_desired_import} was imported, but it should not have been."
            )

    def test_invalid_notebook(self):
        """
        Test that invalid notebook files cannot be imported.
        """
        self.mock_scan_notebooks()
        self.assertRaises(SyntaxError, pipreqs.get_all_imports, self.project_with_invalid_notebooks)

    def test_ipynb_2_py(self):
        """
        Test the function ipynb_2_py() which converts .ipynb file to .py format
        """
        python_imports = pipreqs.get_all_imports(self.python_path_same_imports)
        notebook_imports = pipreqs.get_all_imports(self.notebook_path_same_imports)
        self.assertEqual(python_imports, notebook_imports)

    def test_file_ext_is_allowed(self):
        """
        Test the  function file_ext_is_allowed()
        """
        self.assertTrue(pipreqs.file_ext_is_allowed("main.py", [".py"]))
        self.assertTrue(pipreqs.file_ext_is_allowed("main.py", [".py", ".ipynb"]))
        self.assertFalse(pipreqs.file_ext_is_allowed("main.py", [".ipynb"]))

    def test_parse_requirements(self):
        """
        Test parse_requirements function
        """
        test_cases = [
            (self.empty_filepath, []),  # empty file
            (self.imports_filepath, self.parsed_packages),  # imports with versions
            (
                self.imports_no_version_filepath,
                self.parsed_packages_no_version,
            ),  # imports without versions
            (
                self.imports_any_version_filepath,
                self.parsed_packages_any_version,
            ),  # imports with and without versions
        ]

        for test in test_cases:
            with self.subTest(test):
                filename, expected_parsed_requirements = test

                parsed_requirements = pipreqs.parse_requirements(filename)

                self.assertListEqual(parsed_requirements, expected_parsed_requirements)

    @patch("sys.exit")
    def test_parse_requirements_handles_file_not_found(self, exit_mock):
        captured_output = StringIO()
        sys.stdout = captured_output

        # This assertion is needed, because since "sys.exit" is mocked, the program won't end,
        # and the code that is after the except block will be run
        with self.assertRaises(UnboundLocalError):
            pipreqs.parse_requirements(self.non_existing_filepath)

            exit_mock.assert_called_once_with(1)

            printed_text = captured_output.getvalue().strip()
            sys.stdout = sys.__stdout__

            self.assertEqual(printed_text, "File xpto was not found. Please, fix it and run again.")

    def test_ignore_notebooks(self):
        """
        Test if notebooks are ignored when the scan-notebooks parameter is False
        """
        notebook_requirement_path = os.path.join(self.project_with_notebooks, "requirements.txt")

        pipreqs.init(
            {
                "<path>": self.project_with_notebooks,
                "--savepath": None,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--print": False,
                "--diff": None,
                "--clean": None,
                "--mode": None,
                "--scan-notebooks": False,
            }
        )
        assert os.path.exists(notebook_requirement_path) == 1
        assert os.path.getsize(notebook_requirement_path) == 1    # file only has a "\n", meaning it's empty

    def test_pipreqs_get_imports_from_pyw_file(self):
        pyw_test_dirpath = os.path.join(os.path.dirname(__file__), "_data_pyw")
        requirements_path = os.path.join(pyw_test_dirpath, "requirements.txt")

        pipreqs.init(
            {
                "<path>": pyw_test_dirpath,
                "--savepath": None,
                "--print": False,
                "--use-local": None,
                "--force": True,
                "--proxy": None,
                "--pypi-server": None,
                "--diff": None,
                "--clean": None,
                "--mode": None,
            }
        )

        self.assertTrue(os.path.exists(requirements_path))

        expected_imports = [
            "airflow",
            "matplotlib",
            "numpy",
            "pandas",
            "tensorflow",
        ]

        with open(requirements_path, "r") as f:
            imports_data = f.read().lower()
            for _import in expected_imports:
                self.assertTrue(
                    _import.lower() in imports_data,
                    f"'{_import}' import was expected but not found.",
                )

        os.remove(requirements_path)

    def mock_scan_notebooks(self):
        pipreqs.scan_noteboooks = Mock(return_value=True)
        pipreqs.handle_scan_noteboooks()

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


if __name__ == "__main__":
    unittest.main()
