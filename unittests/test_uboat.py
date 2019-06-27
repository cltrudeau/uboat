import sys
from unittest import TestCase

import uboat
from uboat import flag

# =============================================================================

class GotHere(Exception):
    pass

# Sub-commands to be tested

@uboat.command
def simple(args):
    raise GotHere()


@uboat.command
def responds(args):
    return True


@uboat.command(flag('someparm', nargs='+', help='parm help'), name='complex', 
    help='subcommand help')
def complex_cmd(args):
    raise GotHere()


# -----------------------------------------------------------------------------

class TestUBoat(TestCase):
    def test_simple(self):
        with self.assertRaises(GotHere):
            sys.argv = ['sample.py', 'simple']
            uboat.process_arguments()

    def test_complext(self):
        with self.assertRaises(GotHere):
            sys.argv = ['sample.py', 'complex', 'parm']
            uboat.process_arguments()

    def test_with_flags(self):
        uboat.configure(description='Top level description')
        uboat.configure_subparser(title='sub-commands',
                description='valid sub-commands')
        uboat.add_flags(
            flag('--suffix', action='store_true', 
                help='Adds a sentence after script output'), 
        )

        with self.assertRaises(GotHere):
            sys.argv = ['sample.py', 'simple']
            uboat.process_arguments()

    def test_response(self):
        # other tests use the GotHere() exception which means they don't
        # return properly, this test flows through
        sys.argv = ['sample.py', 'responds']
        args = uboat.process_arguments()
        self.assertIn('func', args)

    def test_badcmd(self):
        # tests a when no command is given
        with self.assertRaises(SystemExit):
            sys.argv = ['sample.py']
            uboat.process_arguments()
