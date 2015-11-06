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

# ASK - What's idiomatic?
def fmt_arg(arg):
    #return arg.upper()
    return '<' + arg.lower() + '>'

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

_DESC_ENCODE = """\
Show the encoding of a message.
"""

_DESC_RUN = """\
Show the operation of the Enigma machine as it encodes a message.
"""

_DESC_STEP = """\
Show the state of the Enigma machine after a specified number of steps.
"""

# TBD - Formats arent all the same: encoding has two more, the encoding and the chunked encoding <<<
# TBD - Combine encode and run, or keep seperate? <<<

# _EPILOG_DISPLAY = """\
# The the number of times '-d' is supplied will determine the level
# of detail displayed:
#     1, which simply shows the specification
#        of the configuration;
#     2, the default, which will show a single line; and
#     3, which will show a detailed schematic of each
#        processing stage
# """

_EPILOG_FORMAT_DISPLAY = """\
The value of {} will determine how a configuration is represented;
possible values include:
    - 'internal', which will show a detailed schematic of each
      processing stage;
    - 'single', the default, which will show a single line;
    - 'windows', just the letters visible at the windows; and
    - 'config', which simply shows the specification
      of the configuration
The program is forgiving about forgotten format values and will accept a range
of reasonable substitutes (e.g., 'detailed' or 'schematic' for 'internal').
"""

# TBD - Have this take lists of actual valid values (e.g., EnigmaConfig._FMTS_INTERNAL) to format
_EPILOG_DISPLAY = _EPILOG_FORMAT_DISPLAY.format(fmt_arg('format'))
_EPILOG_ENCODE = _EPILOG_FORMAT_DISPLAY.format(fmt_arg('format'))





# TBD - Not needed if help can works when in parent
_HELP_ARGS = ['--help', '-h', '-?']
_HELP_KWARGS = {'action': 'help', 'help': 'show this help message and exit'}
_CONFIG_ARGS = ['config']
_CONFIG_KWARGS = {'metavar': fmt_arg('config'), 'action': 'store'}
_DISPLAY_GROUP_KWARGS = {'title': 'display formatting arguments',
                         'description': 'optional arguments for controlling formatting of configurations'}
_FORMAT_ARGS = ['--format', '-f']
_FORMAT_KWARGS = {'metavar': fmt_arg('format'), 'action': 'store', 'nargs': '?', 'default': 'single', 'const': 'single',
                  'help': 'the format used to display configuration(s) (see below)'}
_HIGHLIGHT_ARGS = ['--highlight', '-H']
_HIGHLIGHT_KWARGS = {'metavar': fmt_arg('xy'), 'action': 'store',
                     'help': "a pair or characters to use to bracket encoded characters in a configuration's encoding (see below)"}
_SHOWENCODING_ARGS = ['--showencoding', '-e']
_SHOWENCODING_KWARGS = {'action': 'store_true',
                     'help': "show the encoding if not normally shown"}

if __name__ == '__main__':

    parent_parser = argparse.ArgumentParser(add_help=False)
    # Almost works, but puts config in the wrong position and won't show command help unless theres a config!
    # parent_parser.add_argument('config', metavar=fmt_arg('config'),
    #                             action='store',
    #                             help='the machine configuration to show')
    parent_parser.add_argument('--verbose', '-v',
                               action='store_true',
                               help='display additional information (may have no effect)')
    # show_display_group = parent_parser.add_argument_group(**_DISPLAY_GROUP_KWARGS)
    # _FORMAT_KWARGS['help'] = 'the format to use to show configuration(s) (see below)'
    # show_display_group.add_argument(*_FORMAT_ARGS, **_FORMAT_KWARGS)
    # show_display_group.add_argument(*_HIGHLIGHT_ARGS, **_HIGHLIGHT_KWARGS)
    # show_display_group.add_argument(*_SHOWENCODING_ARGS, **_SHOWENCODING_KWARGS)

    # parent_parser.add_argument('--version', '-V',
    #                            action='version', version='%(prog)s {0}'.format(__version__),
    #                            help='display package version number and exit')
    # parent_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # config_parser = argparse.ArgumentParser(add_help=False)
    # # Almost works, but puts config in the wrong position and won't show command help unless theres a config!
    # config_parser.add_argument('config', metavar=fmt_arg('config'),
    #                             action='store',
    #                             help='the machine configuration to %(dest)s')

    parser = argparse.ArgumentParser(description=_DESC, parents=[parent_parser],
                                     epilog=_EPILOG,
                                     # usage = 'enigma.py [<options>] COMMAND CONFIG',
                                     add_help=False,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    commands = parser.add_subparsers(help='', dest='command',
                                     # title='required arguments',
                                     # description='description, some commands to choose from',
                                     metavar=fmt_arg('command')
                                     )

    # Display machine state
    show_parser = commands.add_parser('show', parents=[parent_parser],
                                      description=_DESC_DISPLAY,
                                      epilog=_EPILOG_DISPLAY,
                                      help='display an Enigma machine configuration',
                                      add_help=False,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    _CONFIG_KWARGS['help'] = 'the machine configuration to show'
    show_parser.add_argument(*_CONFIG_ARGS, **_CONFIG_KWARGS)
    show_display_group = show_parser.add_argument_group(**_DISPLAY_GROUP_KWARGS)
    #_FORMAT_KWARGS['help'] = 'the format to use to show the configuration (see below)'
    show_display_group.add_argument(*_FORMAT_ARGS, **_FORMAT_KWARGS)
    show_display_group.add_argument(*_HIGHLIGHT_ARGS, **_HIGHLIGHT_KWARGS)
    show_display_group.add_argument(*_SHOWENCODING_ARGS, **_SHOWENCODING_KWARGS)
    show_input_group = show_parser.add_argument_group(title='input argument')
    show_input_group.add_argument('--letter', '-l', metavar=fmt_arg('letter'),
                                    action='store', nargs='?', default='', const='',
                                    help='an optional input letter to highlight as it is processed by the '
                                         'configuration, coerced to valid Enigma characters (uppercase letters); '
                                         'defaults to nothing; strings will be truncated at the first letter')
    show_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # Show machine operation
    run_parser = commands.add_parser('run', parents=[parent_parser],
                                      description=_DESC_ENCODE,
                                      epilog=_EPILOG_ENCODE,
                                      help='display enigma machine operation',
                                      add_help=False,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    _CONFIG_KWARGS['help'] = 'the machine setup at the start of operation'
    run_parser.add_argument(*_CONFIG_ARGS, **_CONFIG_KWARGS)

    run_display_group = run_parser.add_argument_group(**_DISPLAY_GROUP_KWARGS)
    #_FORMAT_KWARGS['help'] = 'the format to use to show each configuration (see below)'
    run_display_group.add_argument(*_FORMAT_ARGS, **_FORMAT_KWARGS)
    run_display_group.add_argument(*_HIGHLIGHT_ARGS, **_HIGHLIGHT_KWARGS)
    run_display_group.add_argument(*_SHOWENCODING_ARGS, **_SHOWENCODING_KWARGS)
    run_operation_group = run_parser.add_argument_group(title='run operation arguments',
                                                        description='options for controlling stepping and annotation of steps')
    run_operation_group.add_argument('--noinitial', '-n', dest='initial', action='store_false',
                                     help="don't show the initial starting step as well")
    run_operation_group.add_argument('--overwrite', '-o', action='store_true',
                                     help='overwrite each step')
    run_operation_group.add_argument('--slower', '-S', action='count',
                                   default=0,
                                   help='slow down overwriting (only has effect with --overwrite)')
    run_operation_group.add_argument('--showstep', '-t', action='store_true',
                                     help='show the step number')
    run_operation_group.add_argument('--steps', '-s', metavar=fmt_arg('steps'), action='store',
                                    nargs='?', default=None, const=1, type=int,
                             help='a number of steps to run')
    run_input_group = run_parser.add_argument_group(title='input argument')
    run_input_group.add_argument('--message', '-m', metavar=fmt_arg('message'), action='store',
                                   nargs='?', default=None, const=None,
                             help='a message to encode')
    run_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # Encode a message
    encode_parser = commands.add_parser('encode', parents=[parent_parser],
                                        description=_DESC_ENCODE,
                                        epilog=_EPILOG_ENCODE,
                                        help='encode a message',
                                        add_help=False,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    _CONFIG_KWARGS['help'] = 'the machine setup at the start of encoding'
    encode_parser.add_argument(*_CONFIG_ARGS, **_CONFIG_KWARGS)
    encode_parser.add_argument('message', metavar=fmt_arg('message'), action='store',
                               help='a message to encode')
    encode_display_group = encode_parser.add_argument_group(**_DISPLAY_GROUP_KWARGS)
    _FORMAT_KWARGS['help'] = 'the format to use to show each configuration; see below'
    encode_display_group.add_argument(*_FORMAT_ARGS, action='store_true')
    encode_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # Just show the package version
    _HELP_VERSION = 'Show the package version and exit'
    version_parser = commands.add_parser('version', help=_HELP_VERSION.lower(), add_help=False,
                                         description=_HELP_VERSION + '.')
    version_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

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
        if args.command == 'version':
            print('{0}'.format(__version__))
        else:
            cfg = EnigmaConfig.config_enigma_from_string(args.config)
            fmt = args.format
            sst = args.showstep or args.verbose
            sec = args.showencoding or args.verbose
            mks = (lambda c: args.highlight[0] + c + args.highlight[1]) if args.highlight and len(args.highlight) == 2 else None
            if args.command == 'show':
                if args.verbose:
                    print(unicode(cfg) + ':\n')
                let = args.letter
                print(cfg.config_string(let, fmt, mark_func=mks))
            elif args.command == 'run':
                if args.verbose:
                    print(unicode(cfg) + ':\n')
                cfg.print_operation(message=args.message, steps=args.steps, overwrite=args.overwrite,
                                    format=args.format, initial=args.initial, delay=0.1+(0.1*args.slower),
                                    show_encoding=sec,
                                    show_step=sst,
                                    mark_func=mks)
            elif args.command == 'encode':
                msg = args.message
                if fmt:
                    cfg.print_encoding(msg)
                else:
                    print(cfg.enigma_encoding(msg))
    except EnigmaError as e:
        print(e.message)
        exit(1)




# print(parser.parse_args())
# ASK - Put optional args after required ones? <<<
# http://superuser.com/questions/461946/can-i-use-pipe-output-as-a-shell-script-argument
# ASK - How to test scripts in testing suite? <<<
# From http://bioportal.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/argparse/index.html to start
# Defaults - http://stackoverflow.com/a/15301183/656912

# # ASK - No way to do -ddd as --detail=3? <<<
# show_display_group.add_argument('-d', '--detail', #metavar=fmt_arg('format'), #choices=('internal', 'single', 'config'),
#                             action='count', default=0,  #default=1,
#                             help='the level of detail to show; see below')
