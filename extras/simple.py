#!/usr/bin/env python

import uboat

# ===========================================================================

@uboat.command
def show(args):
    print('This is the "show" sub-command running')

# ===========================================================================

if __name__ == '__main__':
    uboat.process_arguments()
