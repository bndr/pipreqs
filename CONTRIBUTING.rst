============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/bndr/pipreqs/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

pipreqs could always use more documentation, whether as part of the
official pipreqs docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/bndr/pipreqs/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `pipreqs` for local development.

1. Fork the `pipreqs` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pipreqs.git
    $ cd pipreqs/

3. Pipreqs is developed using Poetry. Refer to the `documentation <https://python-poetry.org/docs/>`_ to install Poetry in your local environment. Next, you should install pipreqs's dependencies::

    $ poetry install --with dev

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ poetry run flake8 pipreqs tests
    $ poetry run python -m unittest discover
    $ poetry run tox
    
    To test all versions of python using tox you need to have them installed and for this two options are recommended: `pyenv` or `asdf`.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.8 to 3.11, and PyPy. Check
   https://travis-ci.org/bndr/pipreqs/pull_requests and make sure that the
   tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ poetry run python -m unittest tests.test_pipreqs
