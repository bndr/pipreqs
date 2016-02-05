===============================
``pipreqs`` - Generate requirements.txt file for any project based on imports
===============================

.. image:: https://img.shields.io/travis/bndr/pipreqs.svg
        :target: https://travis-ci.org/bndr/pipreqs
      
        
.. image:: https://img.shields.io/pypi/v/pipreqs.svg
        :target: https://pypi.python.org/pypi/pipreqs

.. image:: https://img.shields.io/pypi/dm/pipreqs.svg
        :target: https://pypi.python.org/pypi/pipreqs
        
.. image:: https://img.shields.io/coveralls/bndr/pipreqs.svg 
        :target: https://coveralls.io/r/bndr/pipreqs
  
        
.. image:: https://img.shields.io/pypi/l/pipreqs.svg 
        :target: https://pypi.python.org/pypi/pipreqs

        

Installation
------------

::

    pip install pipreqs

Usage
-----

::

    Usage:
        pipreqs [options] <path>

    Options:
        --use-local           Use ONLY local package info instead of querying PyPI
        --pypi-server         Use custom PyPi server
        --proxy               Use Proxy, parameter will be passed to requests library. You can also just set the
                              environments parameter in your terminal:
                              $ export HTTP_PROXY="http://10.10.1.10:3128"
                              $ export HTTPS_PROXY="https://10.10.1.10:1080"
        --debug               Print debug information
        --ignore <dirs>...    Ignore extra directories
        --encoding <charset>  Use encoding parameter for file open
        --savepath <file>     Save the list of requirements in the given file
        --force               Overwrite existing requirements.txt

Example
-------

::

    $ pipreqs /home/project/location
    Successfully saved requirements file in /home/project/location/requirements.txt

Contents of requirements.txt

::

    wheel==0.23.0
    Yarg==0.1.9
    docopt==0.6.2
    
Why not pip freeze?
-------------------

- ``pip freeze`` only saves the packages that are installed with ``pip install`` in your environment. 
- pip freeze saves all packages in the environment including those that you don't use in your current project. (if you don't have virtualenv)
- and sometimes you just need to create requirements.txt for a new project without installing modules.
