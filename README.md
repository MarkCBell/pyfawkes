# PyFawkes

PyFawkes is a mutation testing too.
It supports `pytest`_ test in Python 3.5+.

From article at Wikipedia:

    **Mutation testing** (or Mutation analysis or Program mutation)
    evaluates the quality of software tests. Mutation testing involves
    modifying a program's source code or byte code in small ways. A test
    suite that does not detect and reject the mutated code is considered
    defective.

## Quickstart

PyFawkes is available on `PyPI`_, so it can be installed via::

    $ pip install pyfawkes --user --upgrade

Run PyFawkes specifying the location of your code and its unit tests::

    $ python -m pyfawkes --source <PATH TO SOURCE> --test <PATH TO UNIT TESTS>

.. _pytest: https://docs.pytest.org/en/latest/
