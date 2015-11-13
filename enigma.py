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
#from enigma.machine import *
from enigma import *

# ASK - What's idiomatic?
def fmt_arg(arg):
    return arg.upper()
    #return '<' + arg.lower() + '>'


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

_DESC = "A simple Enigma machine simulator with rich display."
_EXAMPLES = """\
Examples:

    $ %(prog)s show "C-II-VIII-I EMO UX.MO.KZ.AY.EF.PL 13.04.11" -l Q -f internal
    $ %(prog)s show "C-II-VIII-I EMO UX.MO.KZ.AY.EF.PL 13.04.11" -lQ -finternal
    $ %(prog)s show "B-I-III-I EMO UX.MO.KZ.AY.EF.PL 13.04.11"
    $ %(prog)s show "$(%(prog)s step 'C-II-VIII-I AAA UX.MO 13.04.11')" -f config

"""
_EPILOG = _EXAMPLES

_HELP_DISPLAY = 'display an Enigma machine configuration'
_DESC_DISPLAY = """\
Show an Enigma machine configuration in the specified format, optionally
indicating the encoding of a specified character.
"""
_EXAMPLES_DSIPLAY = """\
Examples:

    $ %(prog)s TBD

"""
_HELP_DSIPLAY_CONFIG = 'the machine configuration to show'

_HELP_RUN = "show the operation of an Enigma machine"
_DESC_RUN = """\
Show the operation of the Enigma machine as it encodes a message and/or
for a specified number of steps.
"""
_EXAMPLES_RUN = """\
Examples:

    $ %(prog)s TBD

"""
_HELP_RUN_CONFIG = 'the machine setup at the start of operation'

_HELP_ENCODE = "show the encoding of a message"
_DESC_ENCODE = """\
Show the encoding of a message.
"""
_EXAMPLES_ENCODE = """\
Examples:

    $ %(prog)s TBD

"""
_HELP_ENCODE_CONFIG = 'the machine configuration at the start of encoding'

_HELP_VERSION = 'show the package version and exit'
_DESC_VERSION = 'Show the package version and exit.'

_HELP_MESSAGE = 'a message to encode; characters that are not letters will be ' \
                'replaced with standard Naval substitutions or be removed'


_EPILOG_FORMAT_DISPLAY = """\
The value of {fmt_arg} will determine how a configuration is represented;
possible values include:
 + '{fmt_internal_val}', which will show a detailed schematic of each
   processing stage, in which each line corresponds to a component
   of the machine;
 + '{fmt_single_val}', the default, which will show a single line;
 + '{fmt_windows_val}', which shows just the letters visible at the
   windows; and
 + '{fmt_config_val}', which simply shows the specification
   of the configuration
The program is forgiving about forgotten format values and will accept a range
of reasonable substitutes (e.g., {fmt_internal_alts} for {fmt_internal_val}).
""".format(fmt_arg=_FORMAT_KWARGS['metavar'],
           fmt_internal_val=EnigmaConfig._FMTS_INTERNAL[0],
           fmt_single_val=EnigmaConfig._FMTS_SINGLE[0],
           fmt_windows_val=EnigmaConfig._FMTS_WINDOWS[0],
           fmt_config_val=EnigmaConfig._FMTS_CONFIG[0],
           fmt_internal_alts=' or '.join(["'{}'".format(a) for a in EnigmaConfig._FMTS_INTERNAL[1:]]))
_EPILOG_FORMAT_RUN = _EPILOG_FORMAT_DISPLAY

_EPILOG_DISPLAY = _EPILOG_FORMAT_DISPLAY + "\n" + _EXAMPLES_DSIPLAY
_EPILOG_RUN = _EPILOG_FORMAT_RUN + "\n" + _EXAMPLES_RUN
_EPILOG_ENCODE = _EXAMPLES_ENCODE


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
    show_parser = commands.add_parser('show', parents=[parent_parser], add_help=False,
                                      description=_DESC_DISPLAY, epilog=_EPILOG_DISPLAY, help=_HELP_DISPLAY,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    _CONFIG_KWARGS['help'] = _HELP_DSIPLAY_CONFIG
    show_parser.add_argument(*_CONFIG_ARGS, **_CONFIG_KWARGS)
    show_display_group = show_parser.add_argument_group(**_DISPLAY_GROUP_KWARGS)
    show_display_group.add_argument(*_FORMAT_ARGS, **_FORMAT_KWARGS)
    show_display_group.add_argument(*_HIGHLIGHT_ARGS, **_HIGHLIGHT_KWARGS)
    show_display_group.add_argument(*_SHOWENCODING_ARGS, **_SHOWENCODING_KWARGS)
    show_input_group = show_parser.add_argument_group(title='input argument')
    show_input_group.add_argument('--letter', '-l', metavar=fmt_arg('letter'),
                                  action='store', nargs='?', default='', const='',
                                  help='an optional input letter to highlight as it is processed by the '
                                       'configuration; defaults to nothing')
    show_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # Show machine operation
    run_parser = commands.add_parser('run', parents=[parent_parser], add_help=False,
                                     description=_DESC_RUN, epilog=_EPILOG_RUN, help=_HELP_RUN,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    _CONFIG_KWARGS['help'] = _HELP_RUN_CONFIG
    run_parser.add_argument(*_CONFIG_ARGS, **_CONFIG_KWARGS)

    run_display_group = run_parser.add_argument_group(**_DISPLAY_GROUP_KWARGS)
    run_display_group.add_argument(*_FORMAT_ARGS, **_FORMAT_KWARGS)
    run_display_group.add_argument(*_HIGHLIGHT_ARGS, **_HIGHLIGHT_KWARGS)
    run_display_group.add_argument(*_SHOWENCODING_ARGS, **_SHOWENCODING_KWARGS)
    run_operation_group = run_parser.add_argument_group(title='run operation arguments',
                                                        description='options for controlling stepping and '
                                                                    'annotation of steps')
    run_operation_group.add_argument('--noinitial', '-n', dest='initial', action='store_false',
                                     help="don't show the initial starting step")
    run_operation_group.add_argument('--overwrite', '-o', action='store_true',
                                     help='overwrite each step after a pause '
                                          '(may result in garbled output on some systems)')
    run_operation_group.add_argument('--slower', '-S', action='count',
                                     default=0,
                                     help='slow down overwriting; '
                                          'repeat for more slowing (only has effect with --overwrite)')
    run_operation_group.add_argument('--showstep', '-t', action='store_true',
                                     help='show the step number')
    run_operation_group.add_argument('--steps', '-s', metavar=fmt_arg('steps'), action='store',
                                     nargs='?', default=None, const=1, type=int,
                                     help='a number of steps to run; if omitted when a message is provided, '
                                          'will default to the length of the message; otherwise defaults to 1')
    run_input_group = run_parser.add_argument_group(title='input argument')
    run_input_group.add_argument('--message', '-m', metavar=fmt_arg('message'), action='store',
                                 nargs='?', default=None, const=None,
                                 help=_HELP_MESSAGE)
    run_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # Encode a message
    encode_parser = commands.add_parser('encode', parents=[parent_parser], add_help=False,
                                        description=_DESC_ENCODE, epilog=_EPILOG_ENCODE, help=_HELP_ENCODE,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    _CONFIG_KWARGS['help'] = _HELP_ENCODE_CONFIG
    encode_parser.add_argument(*_CONFIG_ARGS, **_CONFIG_KWARGS)
    encode_parser.add_argument('message', metavar=fmt_arg('message'), action='store',
                               help=_HELP_MESSAGE)
    encode_display_group = encode_parser.add_argument_group(**_DISPLAY_GROUP_KWARGS)
    encode_display_group.add_argument(*_FORMAT_ARGS, action='store_true',
                                      help='format the encoded message into blocks')
    encode_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # Just show the package version
    version_parser = commands.add_parser('version', add_help=False,
                                         description=_DESC_VERSION + '.', help=_HELP_VERSION)
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

            if args.command == 'encode':
                msg = args.message
                if fmt:
                    cfg.print_encoding(msg)
                else:
                    print(cfg.enigma_encoding(msg))
            else:
                sst = args.showstep or args.verbose
                sec = args.showencoding or args.verbose
                mks = (lambda c: args.highlight[0] + c + args.highlight[1]) if args.highlight and len(
                    args.highlight) == 2 else None
                if args.command == 'show':
                    if args.verbose:
                        print(unicode(cfg) + ':\n')
                    let = args.letter
                    print(cfg.config_string(let, fmt, mark_func=mks))
                elif args.command == 'run':
                    if args.verbose:
                        print(unicode(cfg) + ':\n')
                    cfg.print_operation(message=args.message, steps=args.steps, overwrite=args.overwrite,
                                        format=args.format, initial=args.initial, delay=0.1 + (0.1 * args.slower),
                                        show_encoding=sec,
                                        show_step=sst,
                                        mark_func=mks)
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
