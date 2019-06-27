#!/usr/bin/env python

import uboat
from uboat import flag

# =================================================================

@uboat.command(
    flag('packages', nargs='+', help='List of packages to add'), 
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
