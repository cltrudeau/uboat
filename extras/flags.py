#!/usr/bin/env python

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
