Build project
=============

Install dependencies ::

    make update-deps

Run tests
=========

There are several ways to run tests

1. Run using `tox` for different virtual environments::

    python3.4 -m tox

2. Use manually for the development purposes mostly, continuously::

    make tests
