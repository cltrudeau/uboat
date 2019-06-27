uboat
*****

This library helps you write command-line python scripts to use sub commands 
(e.g. "git commit", "git checkout"). It is a thin wrapper around the built-in
library argparse.

Installation
============

.. code-block:: bash

    $ pip install uboat

Supports
========

uboat has been tested with Python 3.6 and 3.7

Docs & Source
=============

Docs: http://uboat.readthedocs.io/en/latest/

Source: https://github.com/cltrudeau/uboat

Usage
=====

uboat is a thin wrapper for the sub-parser functionality of the ``argparse``
python library. Creating sub-commands is now as simple as using a decorator.

Example 1: Sub-command Registration
-----------------------------------

The simplest case, creating a single sub-command. Put the following in a file
named "simple.py"


.. code-block:: python

    #!/usr/bin/env python

    import uboat

    # ======================================================================

    @uboat.command
    def show(args):
        print('This is the "show" sub-command running')

    # ======================================================================

    if __name__ == '__main__':
        uboat.process_arguments()


And execution:

.. code-block:: bash

    $ python example.py show
    This is some info

    $ pyton example.py
    usage: example.py [-h] {show} ...

    positional arguments:
      {show}

    optional arguments:
        -h, --help   show this help message and exit

.. _example2:

Example 2: Configuration and Command-line Flags
-----------------------------------------------

uboat also supports passing configuration options to the ``ArgumentParser``
and associated ``subparsers`` objects, this is typically used to improve the
help output. You can also add general flags that go before the sub-command.

Put the following in a file named "flags.py":

.. code-block:: python

    import uboat
    from uboat import flag

    # =================================================================

    @uboat.command
    def greet(args):
        if args.yell:
            print('HELLO!!!!')
        else:
            print('hello')

    # =================================================================

    if __name__ == '__main__':
        uboat.configure(description='A script that greets you')
        uboat.configure_subparser(title='sub-commands',
                description='valid sub-commands')
        uboat.add_flags(
            flag('--yell', action='store_true', 
                help='Makes the greeting louder'), 
        )

        uboat.process_arguments()

You can add one or more ``flag()`` objects to the ``add_flags`` call. The
first parameter of the object is the name of the flag, the rest are keyword
arguments passed through to the ``argparse`` ``add_argument()`` call.

The associated output:

.. code-block:: bash

    $ ./flags.py greet
    hello

    $ ./flags.py --yell greet
    HELOO!!!!!

    $ ./flags.py --help
    usage: flags.py [-h] [--yell] {hello} ...

    A script that greets you

    optional arguments:
      -h, --help  show this help message and exit
      --yell      Makes the greeting louder

    sub-commands:
      valid sub-commands

      {hello}

Example 3: Sub-command Parameters and Flags
-------------------------------------------

Sub-commands can also support arguments and flags. These are handled by adding
information to the registration decorator.

Put the following in a file called "parms.py"

.. code-block:: python

    import uboat
    from uboat import flag

    # =================================================================

    @uboat.command(
        flag('packages', nargs='+', help='Name of package to add'), 
        name='install', help='Pretends to install something')
    def install_cmd(args):
        print('Installing:', ','.join(args.packages))
        print('Done')

    # =================================================================

    if __name__ == '__main__':
        uboat.add_flags(
            flag('--suffix', action='store_true', 
                help='Adds a sentence after script output'), 
        )

        args = uboat.process_arguments()

        if args.suffix:
            print('\nThis is the suffix line')

The above registers a sub-command called "install", notice that the name of
the function in this case isn't the same as the command. Passing the "name"
parameter to the registration decorator overrides the use of the function name
as the sub-command. The registration decorator uses the same ``flag()``
concept as the ``add_flags()`` call explained in :ref:`example2`. The flags in
the decorator are just passed through to the ``argparse`` ``add_argument()``
call and so can be either parameters or flags depending on the keyword
arguments.

The ``process_arguments()`` call returns a reference to the ``argparse``
``Namespace`` object and so can be checked after the sub-command has run.

The above example in usage:

.. code-block:: bash

    $ ./parms.py
    usage: parms.py [-h] [--suffix] {install} ...

    positional arguments:
      {install}
	install   Pretends to install something

    optional arguments:
      -h, --help  show this help message and exit
      --suffix    Adds a sentence after script output

    $ ./parms.py install
    usage: parms.py install [-h] packages [packages ...]
    parms.py install: error: the following arguments are required: packages

    $ ./parms.py install foo
    Installing: foo
    Done

Example Source
--------------

Source code for the above examples is available in the source code repository:

Source: https://github.com/cltrudeau/uboat/tree/master/extras

