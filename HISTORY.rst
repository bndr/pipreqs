.. :changelog:

History
-------

0.4.4 (2016-07-14)
---------------------

* Remove Spaces in output
* Add package to output even without version

0.4.2 (2016-02-10)
---------------------

* Fix duplicated lines in requirements.txt (Dmitry Pribysh)

0.4.1 (2016-02-05)
---------------------

* Added ignore option (Nick Rhinehart)

0.4.0 (2016-01-28)
---------------------

* Walk Abstract Syntax Tree to find imports (Kay Sackey)

0.3.9 (2016-01-20)
---------------------

* Fix regex for docstring comments (#35)

0.3.8 (2016-01-12)
---------------------

* Add more package mapping
* fix(pipreqs/mapping): remove pylab reference to matplotlib
* Remove comments """ before going through imports
* Update proxy documentation

0.3.1 (2015-10-20)
---------------------

* fixed lint warnings (EJ Lee)
* add --encoding parameter for open() (EJ Lee)
* support windows directory separator (EJ Lee)

0.3.0 (2015-09-29)
---------------------

* Add --proxy option
* Add --pypi-server option

0.2.9 (2015-09-24)
---------------------

* Ignore irreverent directory when generating requirement.txt (Lee Wei)
* Modify logging level of "Requirement.txt already exists" to warning (Lee Wei)

0.2.8 (2015-05-11)
---------------------

* Add --force option as a protection for overwrites

0.2.6 (2015-05-11)
---------------------

* Fix exception when 'import' is used inside package name #17
* Add more tests

0.2.5 (2015-05-11)
---------------------

* Fix exception when 'import' is used in comments #17
* Fix duplicate entries in requirements.txt

0.2.4 (2015-05-10)
---------------------

* Refactoring
* fix "import as"

0.2.3 (2015-05-09)
---------------------

* Fix multiple alias imports on the same line (Tiago Costa)
* More package mappings

0.2.2 (2015-05-08)
---------------------

* Add ImportName -> PackageName mapping
* More tests

0.2.1 (2015-05-08)
---------------------

* Fix for TypeError for implicit conversion

0.2.0 (2015-05-06)
---------------------

* Add --use-local option
* Exclude relative imports. (Dongwon Shin)
* Use "latest_release_id" instead of "release_ids[-1]" (Dongwon Shin)

0.1.9 (2015-05-01)
---------------------

* Output tuning (Harri Berglund)
* Use str.partition() to simplify the logic (cclaus)

0.1.8 (2015-04-26)
---------------------

* Fixed problems with local imports (Dongwon Shin)
* Fixed problems with imports with 'as' (Dongwon Shin)
* Fix indentation, pep8 Styling. (Michael Borisov)
* Optimize imports and adding missing import for sys module. (Michael Borisov)

0.1.7 (2015-04-24)
---------------------

* Add more assertions in tests
* Add more verbose output
* Add recursive delete to Makefile clean
* Update Readme

0.1.6 (2015-04-22)
---------------------

* py3 print function

0.1.5 (2015-04-22)
---------------------

* Add Readme, Add Examples
* Add Stdlib into package

0.1.1 (2015-04-22)
---------------------

* Fix regex matching for imports
* Release on Pypi

0.1.0 (2015-04-22)
---------------------

* First release on Github.
