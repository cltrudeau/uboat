__version__ = '0.1.0'

import argparse
from functools import wraps

# =============================================================================

class Flag:
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.kwargs = kwargs
    

class SubCommand:
    def __init__(self, name):
        self.name = name
        self.flags = []
        self.kwargs = {}
        self.func = None


class CommandManager:
    def __init__(self):
        self.flags = []
        self.config = {}
        self.sub_config = {}
        self.sub_commands = []


def flag(name, **kwargs):
    """Function acts like a wrapper for flag parameters that would be used
    inside of a argparse.add_argument() call"""
    return Flag(name, **kwargs)


def add_flags(*args):
    """Registers command line flags with the CommandManager."""
    manager.flags.extend(args)


def configure(**kwargs):
    """Registers configuration parameters for the ArgumentParser"""
    manager.config = kwargs


def configure_subparser(**kwargs):
    """Registers configurtion parameters for the subparser created inside the
    ArgumentParser."""
    manager.sub_config = kwargs


# -----------------------------------------------------------------------------
# Sub-command Parser
# -----------------------------------------------------------------------------

def process_arguments():
    # create the parser and subparsers
    parser = argparse.ArgumentParser(**manager.config)
    subparser = parser.add_subparsers(**manager.sub_config)

    #import pudb; pudb.set_trace()

    # for each flag (for the command line, not for the sub-commands), add them
    # to the parser
    for flag in manager.flags:
        parser.add_argument(flag.name, **flag.kwargs)

    # for each cmd, register it with the parser
    for cmd in manager.sub_commands:
        # create the sub-parser
        cmd_parser = subparser.add_parser(cmd.name, **cmd.kwargs)

        # if there were flags defined for the sub-command, add them
        for flag in cmd.flags:
            cmd_parser.add_argument(flag.name, **flag.kwargs)

        # register the function to be called when the command is invoked
        cmd_parser.set_defaults(func=cmd.func)

    # everything should be registered and ready to go, call the actual parser
    args = parser.parse_args()

    # since this library is for sub-commands, we can assume you must give a
    # sub-command
    if not hasattr(args, 'func'):
        parser.print_help()
        exit()

    # execute the function associated with the command and then return the
    # argument Namespace from the parser
    args.func(args)
    return args


# -----------------------------------------------------------------------------
# Command Registration Decorator
# -----------------------------------------------------------------------------

def command(*decorator_args, **decorator_kwargs):
    """Decorator for registering new sub-commands.

    Can be called with or without parameters
    """
    called_with_parms = True
    if len(decorator_args) == 1 and callable(decorator_args[0]):
        # decorator can be of form "@smear", or "@smear('stuff')"
        # in the first case there will only one argument and it will be
        # the wrapped function
        called_with_parms = False

    def decorator(method):
        cmd = SubCommand(method.__name__)

        if 'name' in decorator_kwargs:
            # user provided an alternate name, use that and remove it from
            # the calling dict
            cmd.name = decorator_kwargs['name']
            del decorator_kwargs['name']

        if called_with_parms:
            # only add the decorator_args if this was called with parameters,
            # otherwise that variable contains the calling method
            cmd.flags = decorator_args

        cmd.kwargs = decorator_kwargs
        cmd.func = method

        manager.sub_commands.append(cmd)

        @wraps(method)
        def wrapper(*args, **kwargs):
            print('%%%%')
            return method(*args, **kwargs)
        return wrapper

    #if len(decorator_args) == 1 and callable(decorator_args[0]):
    if not called_with_parms:
        return decorator(*decorator_args, **decorator_kwargs)

    return decorator

# =============================================================================

manager = CommandManager()
