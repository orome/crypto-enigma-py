#!/usr/bin/env python
# encoding: utf8

""" 
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)

import argparse

from enigma import __version__
from enigma.machine import *

_DESC = "A simple Enigma machine simulator with rich display."

_EPILOG = """\
Examples:

    $ %(prog)s show "C-II-VIII-I EMO UX.MO.KZ.AY.EF.PL 13.04.11" -l Q -f internal
    $ %(prog)s show "C-II-VIII-I EMO UX.MO.KZ.AY.EF.PL 13.04.11" -lQ -finternal
    $ %(prog)s show "B-I-III-I EMO UX.MO.KZ.AY.EF.PL 13.04.11"
    $ %(prog)s show "$(%(prog)s step 'C-II-VIII-I AAA UX.MO 13.04.11')" -f config


"""

_DESC_DISPLAY = """\
Show an Enigma machine configuration in the specified format, optionally
indicating the encoding of a specified character.
"""

# _EPILOG_DISPLAY = """\
# The the number of times '-d' is supplied will determine the level
# of detail displayed:
#     1, which simply shows the specification
#        of the configuration;
#     2, the default, which will show a single line; and
#     3, which will show a detailed schematic of each
#        processing stage
# """

_EPILOG_DISPLAY = """\
The selection for '--format' will determine what is shown; options include:
    - 'internal', which will show a detailed schematic of each
      processing stage;
    - 'single', which will show a single line;
    - 'windows', just the letters visible at the windows; and
    - 'config', the default, which simply shows the specification
      of the configuration
"""

# TBD - Not needed if help can works when in parent
_HELP_ARGS = ['--help', '-h', '-?']
_HELP_KWARGS = {'action': 'help', 'help': 'show this help message and exit'}


# ASK - What's idiomatic?
def fmt_arg(arg):
    return arg.upper()
    # return '<' + arg.lower() + '>'

if __name__ == '__main__':

    parent_parser = argparse.ArgumentParser(add_help=False)
    # Almost works, but puts config in the wrong position and won't show command help unless theres a config!
    # parent_parser.add_argument('config', metavar=fmt_arg('config'),
    #                             action='store',
    #                             help='the machine configuration to show')
    parent_parser.add_argument('--verbose', '-v',
                               action='store_true',
                               help='display additional information (may have no effect)')
    parent_parser.add_argument('--version', '-V',
                               action='version', version='%(prog)s {0}'.format(__version__),
                               help='display package version number and exit')
    # parent_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    parser = argparse.ArgumentParser(description=_DESC, parents=[parent_parser],
                                     epilog=_EPILOG,
                                     # usage = 'xyz',
                                     add_help=False,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    subparsers = parser.add_subparsers(help='', dest='command',
                                       title='required arguments',
                                       description='description, some commands to choose from',
                                       metavar=fmt_arg('command')
                                       )

    # Display machine state
    show_parser = subparsers.add_parser('show', parents=[parent_parser],
                                        description=_DESC_DISPLAY,
                                        epilog=_EPILOG_DISPLAY,
                                        help='display an Enigma machine configuration',
                                        add_help=False,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    show_parser.add_argument('config', metavar=fmt_arg('config'),
                             action='store',
                             help='the machine configuration to show')
    show_display_group = show_parser.add_argument_group(title="display arguments", description="some display arguments")
    show_display_group.add_argument('--format', '-f', metavar=fmt_arg('format'),
                                    # choices=('internal', 'single', 'config'),
                                    action='store', nargs='?', default='single', const='single',
                                    help='the format to use to show the configuration; see below')

    show_display_group.add_argument('--letter', '-l', metavar=fmt_arg('letter'),
                                    action='store', nargs='?', default='', const='',
                                    help='an optional input letter to highlight as it is processed by the '
                                         'configuration, coerced to valid Enigma characters (uppercase letters); '
                                         'defaults to nothing; strings will be truncated at the first letter')
    show_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)
    # group = parser.add_mutually_exclusive_group()

    # Encode a message
    encode_parser = subparsers.add_parser('encode', help='encode a message', parents=[parent_parser], add_help=False)
    encode_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)


    # Show machine operation
    run_parser = subparsers.add_parser('run', help='display machine operation', parents=[parent_parser], add_help=False)
    run_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # Show machine operation
    step_parser = subparsers.add_parser('step', help='step the configuration once', parents=[parent_parser], add_help=False)
    step_parser.add_argument('config', metavar=fmt_arg('config'),
                             action='store',
                             help='the machine to start with')
    step_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)


    # try:
    #     args = parser.parse_args()
    # # ASK - How to catch just wrong argument errors <<<
    # # ASK - How to print help for current subcommand, if there is one <<<
    # except:# argparse.ArgumentError as e:
    #     parser.print_help()
    #     exit(0)
    # else:

    args = parser.parse_args()

    try:
        cfg = EnigmaConfig.config_enigma_from_string(args.config)
    except EnigmaError as e:
        print(e.message)
        exit(0)
    else:
        # TBD - Add encoding note to config and windows (e.g with P > K) <<<
        # TBD - Add components format that lists the components and their attributes <<<
        if args.command == 'show':
            format = args.format
            let = args.letter
            if format in ['internal']:
                print(cfg.config_string_internal(let))
            elif format in ['single']:
                print(cfg.config_string(let))
            # # TBD - Another version that prints spec on individual lines; or list or elements?
            elif format in ['windows']:
                print(cfg.windows())
            elif format in ['config']:
                print(cfg)
            # Hidden option for debugging
            elif format in ['debug']:
                print(cfg.__repr__())
            else:
                print('?')
        # TBD - Should share same arguments and same stucture with show <<<
        elif args.command == 'step':
            print(cfg.step())


# import argparse
#
# parser = argparse.ArgumentParser()
#
# # Put common subparser arguments here. Each sub parser will have
# # its own -h option, so disable it on the shared base.
# subbase = argparse.ArgumentParser(add_help=False)
# subbase.add_argument('config', metavar='CONFIG', action='store', help='the config to use')
#
# subparsers = parser.add_subparsers(help='', dest='command',  metavar='COMMAND', title='required arguments',
#                                    description='two arguments are required')
#
# # Add subbase to the parent list for each subparser.
# cmda_parser = subparsers.add_parser('cmdA', parents=[subbase],  help='a first command')
# cmdb_parser = subparsers.add_parser('cmdB', parents=[subbase], help='the second operation')
# cmdc_parser = subparsers.add_parser('cmdC', parents=[subbase], help='yet another thing')
#
# print(parser.parse_args())

# import argparse
#
# parser = argparse.ArgumentParser()
#
# subparsers = parser.add_subparsers(help='', dest='command',  metavar='COMMAND'
# # title='required arguments',
# #                                    description='two arguments are required'
# )
# parser.add_argument('config', metavar='CONFIG', action='store', help='the config to use')
#
# cmda_parser = subparsers.add_parser('cmdA',  help='a first command')
# cmdb_parser = subparsers.add_parser('cmdB',  help='the second operation')
# cmdc_parser = subparsers.add_parser('cmdC',  help='yet another thing')
#
# print(parser.parse_args())
# ASK - How to reverse help help (--help, -h) and add -? <<<
# http://superuser.com/questions/461946/can-i-use-pipe-output-as-a-shell-script-argument
# ASK - How to test scripts in testing suite? <<<
# From http://bioportal.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/argparse/index.html to start
# Defaults - http://stackoverflow.com/a/15301183/656912

# # ASK - No way to do -ddd as --detail=3? <<<
# show_display_group.add_argument('-d', '--detail', #metavar=fmt_arg('format'), #choices=('internal', 'single', 'config'),
#                             action='count', default=0,  #default=1,
#                             help='the level of detail to show; see below')
