=================================
Trimports - Remove Unused Imports
=================================

Trimports is a program which automatically removes unused imports from your Python script.

Install
-------

From PyPI :

    $ pip install trimports

Usage: trimports [-h] -l/--location "<FILE_LOCATION>"

required arguments:
-------------------

 > -h, --help            show this help message and exit. \
 > -l FILE_LOCATION,
 > --location FILE_LOCATION   Location of Target file.
 
Example: 
--------

 1. `trimports -l "/home/Documents/Python/utils.py"`
 2. `trimports --location "/home/Documents/Python/utils.py"`

