#!/usr/bin/env python

import uboat
from uboat import flag

# ===========================================================================

people = ['Bob', 'Brenda', 'Gail']

# ---------------------------------------------------------------------------

@uboat.command(flag('person', nargs='+', help='Name of person to add'), 
    name='add', help='Pretends to add a name to the list of people')
def add_cmd(args):
    print('Adding name(s):', ','.join(args.person))
    print('Name added')


@uboat.command
def list(args):
    print('The list contains:')
    for person in people:
        if args.filter:
            if not person.startswith(args.filter):
                continue

        print('   ', person)


# ===========================================================================

if __name__ == '__main__':
    uboat.configure(description='Pretend name list manipulator')
    uboat.configure_subparser(title='sub-commands',
            description='valid sub-commands')
    uboat.add_flags(
        flag('--suffix', action='store_true', 
            help='Adds a sentence after script output'), 
        flag('--filter', help='A "startswith" filter for the output'),
    )

    args = uboat.process_arguments()

    if args.suffix:
        print('\nThis is the suffix line')
