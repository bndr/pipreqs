===============================
``pipreqs`` - Generate requirements.txt file for any project based on imports
===============================

.. image:: https://img.shields.io/travis/bndr/pipreqs.svg
        :target: https://travis-ci.org/bndr/pipreqs

.. image:: https://img.shields.io/pypi/v/pipreqs.svg
        :target: https://pypi.python.org/pypi/pipreqs

Installation
------------

::

    pip install pipreqs

Usage
-----

::

    Usage:
        pipreqs <path> [options]

    Options:
    	--savepath Supply custom path for requirements.txt
        --debug    See debug output

Example
-------

::

    $ pipreqs /home/project/location
    Successfuly saved requirements file in: /home/project/location/requirements.txt
 

Why not pip freeze?
--------
