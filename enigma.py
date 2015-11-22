#!/usr/bin/env python
# encoding: utf8

# Copyright (C) 2015 by Roy Levien.
# This file is part of crypto-enigma, an Enigma Machine simulator.
# released under the BSD-3 License (see LICENSE.txt).

""" 
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)

import argparse

from crypto_enigma import __version__
from crypto_enigma import *


# Decode the Enigma specification string
# http://stackoverflow.com/q/33811930/; http://stackoverflow.com/q/22947181/
def unicode_literal(str_, encoding=sys.stdin.encoding):
    if not isinstance(str_, unicode):
        return str_.decode(encoding)
    else:
        return str_


# ASK - What's idiomatic?
def fmt_arg(arg):
    return arg.upper()
    # return '<' + arg.lower() + '>'


def make_args(name, is_opt=False, opt_letter=None):
    if not is_opt:
        return name
    else:
        return ['--' + name, '-' + (opt_letter if opt_letter is not None else name[0])]


_HELP_ARGS = ['--help', '-h', '-?']
_HELP_KWARGS = dict(
    action='help',
    help='show this help message and exit')

_CONFIG_ARGS = ['config']
_CONFIG_KWARGS = dict(
    action='store', metavar=fmt_arg('config'),
    type=unicode_literal)

_MESSAGE_HELP = 'a message to encode; characters that are not letters will be ' \
                'replaced with standard Naval substitutions or be removed'
_ENCODE_MESSAGE_NAME = 'message'
_ENCODE_MESSAGE_ARG = make_args(_ENCODE_MESSAGE_NAME)
_ENCODE_MESSAGE_KWARGS = dict(
    action='store', metavar=fmt_arg(_ENCODE_MESSAGE_NAME),
    help=_MESSAGE_HELP)
_RUN_MESSAGE_ARGS = make_args(_ENCODE_MESSAGE_NAME, True)
_RUN_MESSAGE_KWARGS = dict(
    action='store', metavar=fmt_arg(_ENCODE_MESSAGE_NAME), nargs='?', default=None, const=None,
    help=_MESSAGE_HELP)

_LETTER_NAME = 'letter'
_LETTER_ARGS = make_args(_LETTER_NAME, True)
_LETTER_KWARGS = dict(
    action='store', metavar=fmt_arg(_LETTER_NAME), nargs='?', default='', const='',
    help='an optional input letter to highlight as it is processed by the configuration; defaults to nothing')

_DISPLAY_GROUP_KWARGS = dict(
    title='display formatting arguments',
    description='optional arguments for controlling formatting of machine configurations')

_FORMAT_NAME = 'format'
_FORMAT_ARGS = make_args(_FORMAT_NAME, True)
_FORMAT_KWARGS = dict(
    action='store', metavar=fmt_arg(_FORMAT_NAME), nargs='?', default='single', const='single',
    help='the format used to display machine configuration(s) (see below)')

_HIGHLIGHT_NAME = 'highlight'
_HIGHLIGHT_ARGS = make_args(_HIGHLIGHT_NAME, True, 'H')
_HIGHLIGHT_KWARGS = dict(
    action='store', metavar=fmt_arg('hh'),
    help="a pair or characters to use to highlight encoded characters in a machine configuration's encoding "
         "(see below)")

_SHOWENCODING_NAME = 'showencoding'
_SHOWENCODING_ARGS = make_args(_SHOWENCODING_NAME, True, 'e')
_SHOWENCODING_KWARGS = dict(
    action='store_true',
    help='show the encoding if not normally shown for the specified ' + _FORMAT_KWARGS['metavar'])

_DESC = "A simple Enigma machine simulator with rich display of machine configurations."
_EXAMPLES = """\
Examples:

    $ %(prog)s encode "B-I-III-I EMO UX.MO.AY 13.04.11" "TESTINGXTESTINGUD"
    $ %(prog)s encode "B-I-III-I EMO UX.MO.AY 13.04.11" "TESTINGXTESTINGUD" -f
    $ %(prog)s encode "B-I-III-I EMO UX.MO.AY 13.04.11" "TESTING! testing?" -f
    $ %(prog)s show "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X'
    $ %(prog)s show "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X' -H'()'
    $ %(prog)s show "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X' -H'()' -f internal
    $ %(prog)s run "B-I-III-I EMO UX.MO.AY 13.04.11" -s 10 -t
    $ %(prog)s run "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -H'()'
    $ %(prog)s run "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -H'()' -f internal
    $ %(prog)s run "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -H'()' -f internal -o -SS
    $ %(prog)s run "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -f config -e
    $ %(prog)s run "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -f internal -e
    $ %(prog)s run "c-β-VIII-VII-VI QMLI UX.MO.AY 01.13.04.11" -s 500 -t -f internal -o


More information about each of these examples is available in the help for the respective
commands.

"""
_EPILOG = _EXAMPLES

# Encode command help strings
_HELP_ENCODE = "show the encoding of a message"
_DESC_ENCODE = """\
Show the encoding of a message.
"""
_EXAMPLES_ENCODE = """\
Examples:

  Encode a message:
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" "TESTINGXTESTINGUD"
    OZQKPFLPYZRPYTFVU
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" "OZQKPFLPYZRPYTFVU"
    TESTINGXTESTINGUD

  Encode a message and break the output into blocks of 4:
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" "TESTINGXTESTINGUD" -f
    OZQK PFLP YZRP YTFV U

  Standard Naval subistitutions for non-letter characters are performed
  before encoding:
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" "TESTING! testing?" -f
    OZQK PFLP YZRP YTFV U

"""
_HELP_ENCODE_CONFIG = 'the machine configuration at the start of encoding (see below)'

# Show command help strings
_HELP_SHOW = 'display an Enigma machine configuration'
_DESC_SHOW = """\
Show an Enigma machine configuration in the specified format, optionally
indicating the encoding of a specified character.
"""
_EXAMPLES_SHOW = """\
Examples:

  Show an Enigma machine configuration as its mapping (see '{fmt_single_val}'
  in the note on {fmt_arg}), followed by the window letters and ring settings,
  and indicate how a letter is encoded; here X is encoded to T (A would be
  encoded to C, B to N ... Y to W, Z to O):
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X'
    X > CNAUJVQSLEMIKBZRGPHXDFYT̲̅WO  EMO  19 10 05

  Use an alternate method for highlighting the encoded-to letter:
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X' -H'()'
    X > CNAUJVQSLEMIKBZRGPHXDFY(T)WO  EMO  19 10 05

  Show a detailed stage-by-stage schematic (see '{fmt_internal_val}' in the note
  on {fmt_arg}) of the mappings preformed by a configuration:
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X' -H'()' -f {fmt_internal_val}
    X > ABCDEFGHIJKLMNOPQRSTUVW(X)YZ
      P YBCDEFGHIJKLONMPQRSTXVW(U)AZ         UX.MO.AY
      1 HCZMRVJPKSUDTQOLWEXN(Y)FAGIB  O  05  I
      2 KOMQEPVZNXRBDLJHFSUWYACT(G)I  M  10  III
      3 AXIQJZ(K)RMSUNTOLYDHVBWEGPFC  E  19  I
      R YRUHQSLDPX(N)GOKMIEBFZCWVJAT         B
      3 ATZQVYWRCEGOI(L)NXDHJMKSUBPF         I
      2 VLWMEQYPZOA(N)CIBFDKRXSGTJUH         III
      1 WZBLRVXAYGIPD(T)OHNEJMKFQSUC         I
      P YBCDEFGHIJKLONMPQRS(T)XVWUAZ         UX.MO.AY
    T < CNAUJVQSLEMIKBZRGPHXDFY(T)WO

  Just show the configuration in conventional format (as used in {cfg_arg}):
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X' -f {fmt_config_val}
    B-I-III-I EMO UX.MO.AY 13.04.11

  As above, but show the encoding too (not shown my default for '{fmt_config_val}'):
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X' -f {fmt_config_val} -e
    B-I-III-I EMO UX.MO.AY 13.04.11  X > T

"""
_HELP_DSIPLAY_CONFIG = 'the machine configuration to show (see below)'

# Run command help strings
_HELP_RUN = "show the operation of an Enigma machine"
_DESC_RUN = """\
Show the operation of the Enigma machine as a series of configurations, as it
encodes a message and/or for a specified number of steps.
"""
_EXAMPLES_RUN = """\
Examples:

(For details on differences among formats used for displaying each step, see the
examples in the help for the '{shw_cmd}' command.)

  Show the operation of a machine for 10 steps, indicating step numbers (see
  '{fmt_single_val}' in the note on {fmt_arg}):
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -s 10 -t
    0000      CNAUJVQSLEMIKBZRGPHXDFYTWO  EMO  19 10 05
    0001      UNXKGVERLYDIQBTWMHZOAFPCJS  EMP  19 10 06
    0002      QTYJZXUPKDIMLSWHAVNBGROFCE  EMQ  19 10 07
    0003      DMXAPTRWKYINBLUESGQFOZHCJV  ENR  19 11 08
    0004      IUSMHRPEAQTVDYWGJFCKBLOZNX  ENS  19 11 09
    0005      WMVXQRLSPYOGBTKIEFHNZCADJU  ENT  19 11 10
    0006      WKIQXNRSCVBOYFLUDGHZPJAEMT  ENU  19 11 11
    0007      RVPTWSLKYXHGNMQCOAFDZBEJIU  ENV  19 11 12
    0008      IYTKRVSMALDJHZWXUEGCQFOPBN  ENW  19 11 13
    0009      PSWGMODULZVIERFAXNBYHKCQTJ  ENX  19 11 14
    0010      IVOWZKHGARFSPUCMXJLYNBDQTE  ENY  19 11 15

  Show the operation of a machine as it encodes a message, with step numbers:
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -H'()'
    0000       CNAUJVQSLEMIKBZRGPHXDFYTWO   EMO  19 10 05
    0001  T > UNXKGVERLYDIQBTWMHZ(O)AFPCJS  EMP  19 10 06
    0002  E > QTYJ(Z)XUPKDIMLSWHAVNBGROFCE  EMQ  19 10 07
    0003  S > DMXAPTRWKYINBLUESG(Q)FOZHCJV  ENR  19 11 08
    0004  T > IUSMHRPEAQTVDYWGJFC(K)BLOZNX  ENS  19 11 09
    0005  I > WMVXQRLS(P)YOGBTKIEFHNZCADJU  ENT  19 11 10
    0006  N > WKIQXNRSCVBOY(F)LUDGHZPJAEMT  ENU  19 11 11
    0007  G > RVPTWS(L)KYXHGNMQCOAFDZBEJIU  ENV  19 11 12

  Show the operation of a machine as it encodes a message in more detail (see
  '{fmt_internal_val}' in the note on {fmt_arg}), with step numbers (only some
  steps shown here):
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -H'()' -f {fmt_internal_val}
    0000
    ...
    0001
    T > ABCDEFGHIJKLMNOPQRS(T)UVWXYZ
      P YBCDEFGHIJKLONMPQRS(T)XVWUAZ         UX.MO.AY
      1 BYLQUIOJRTCSPNKVDWM(X)EZFHAG  P  06  I
      2 KOMQEPVZNXRBDLJHFSUWYAC(T)GI  M  10  III
      3 AXIQJZKRMSUNTOLYDHV(B)WEGPFC  E  19  I
      R Y(R)UHQSLDPXNGOKMIEBFZCWVJAT         B
      3 ATZQVYWRCEGOILNXD(H)JMKSUBPF         I
      2 VLWMEQY(P)ZOANCIBFDKRXSGTJUH         III
      1 YAKQUWZXFHOCSNG(M)DILJEPRTBV         I
      P YBCDEFGHIJKL(O)NMPQRSTXVWUAZ         UX.MO.AY
    O < UNXKGVERLYDIQBTWMHZ(O)AFPCJS
    ...
    0007
    G > ABCDEF(G)HIJKLMNOPQRSTUVWXYZ
      P YBCDEF(G)HIJKLONMPQRSTXVWUAZ         UX.MO.AY
      1 IDLNWM(J)HEPXQGRYTZBUAVSFKOC  V  12  I
      2 NLPDOUYMW(Q)ACKIGERTVXZBSFHJ  N  11  III
      3 AXIQJZKRMSUNTOLY(D)HVBWEGPFC  E  19  I
      R YRU(H)QSLDPXNGOKMIEBFZCWVJAT         B
      3 ATZQVYW(R)CEGOILNXDHJMKSUBPF         I
      2 KVLDPXOYNZMBHAECJ(Q)WRFSITGU         III
      1 TRZBIWMHAGXCFDYJ(L)NVPSUEKOQ         I
      P YBCDEFGHIJK(L)ONMPQRSTXVWUAZ         UX.MO.AY
    L < RVPTWS(L)KYXHGNMQCOAFDZBEJIU

  Show the steps as above, but (slowly) in place (if the platform supports it)
  rather than on a new line for each; only the last step is visible on
  completion (as shown here):
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -H'()' -f {fmt_internal_val} -o -SS
    0007
    G > ABCDEF(G)HIJKLMNOPQRSTUVWXYZ
      P YBCDEF(G)HIJKLONMPQRSTXVWUAZ         UX.MO.AY
      1 IDLNWM(J)HEPXQGRYTZBUAVSFKOC  V  12  I
      2 NLPDOUYMW(Q)ACKIGERTVXZBSFHJ  N  11  III
      3 AXIQJZKRMSUNTOLY(D)HVBWEGPFC  E  19  I
      R YRU(H)QSLDPXNGOKMIEBFZCWVJAT         B
      3 ATZQVYW(R)CEGOILNXDHJMKSUBPF         I
      2 KVLDPXOYNZMBHAECJ(Q)WRFSITGU         III
      1 TRZBIWMHAGXCFDYJ(L)NVPSUEKOQ         I
      P YBCDEFGHIJK(L)ONMPQRSTXVWUAZ         UX.MO.AY
    L < RVPTWS(L)KYXHGNMQCOAFDZBEJIU

  Stepping a configuration only changes the window letters:
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -f {fmt_config_val} -e
    000  B-I-III-I EMO UX.MO.AY 13.04.11
    0001  B-I-III-I EMP UX.MO.AY 13.04.11  T > O
    0002  B-I-III-I EMQ UX.MO.AY 13.04.11  E > Z
    0003  B-I-III-I ENR UX.MO.AY 13.04.11  S > Q
    0004  B-I-III-I ENS UX.MO.AY 13.04.11  T > K
    0005  B-I-III-I ENT UX.MO.AY 13.04.11  I > P
    0006  B-I-III-I ENU UX.MO.AY 13.04.11  N > F
    0007  B-I-III-I ENV UX.MO.AY 13.04.11  G > L
    $ %(prog)s "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -f {fmt_windows_val} -e
    0000  EMO
    0001  EMP  T > O
    0002  EMQ  E > Z
    0003  ENR  S > Q
    0004  ENS  T > K
    0005  ENT  I > P
    0006  ENU  N > F
    0007  ENV  G > L

   Watch the machine run for 500 steps:
    $ %(prog)s "c-β-VIII-VII-VI QMLI UX.MO.AY 01.13.04.11" -s 500 -t -f internal -o

"""
_HELP_RUN_CONFIG = 'the machine setup at the start of operation (see below)'

# Version command help strings
_HELP_VERSION = 'show the package version and exit'
_DESC_VERSION = 'Show the package version and exit.'


_EPILOG_CONFIG = """\
{cfg_arg} specifies an Enigma machine configuration as a string based on common
historical conventions and consists of four elements, separated by spaces:
 + names for components, in physical order (starting with the reflector, on the
   left, and ending with the 'first' rotor, on the right), separated by '-'s;
 + letters visible at the machine windows (in physical order);
 + a plugboard specification, consisting of exchanged (i.e. wired-together)
   letter paris, separated by '.'s; and
 + the locations of ring letter A on the rotor for each rotor
   (in physical order)
"""

_EPILOG_FORMAT = """\
{fmt_arg} will determine how a configuration is represented; possible values
include:
 + '{fmt_single_val}' (the default) which will show a single line representing the
   mapping (a string in which the letter at each position indicates the letter
   encoded to by letter at that position in the alphabet) preformed by the
   machine as a whole, followed by window letters (as '{fmt_windows_val}') and
   positions, and indicating a {let_arg} and its encoding, if provided;
 + '{fmt_internal_val}', which will show a detailed schematic of each processing step
   (proceeding from top to bottom), in which
    - each line indicates the mapping (see '{fmt_single_val}') preformed by the
      component at that step;
    - each line begins with an indication of the stage (rotor number, "P" for
      plugboard, or "R" for reflector) at that step, and ends with the
      specification of the component at that stage;
    - rotors also indicate their window letter, and position;
    - if a valid {let_arg} is provided, it is indicated as input and its
      encoding at each stage is marked;
   the schematic is followed by the mapping for the machine as a whole (as
   '{fmt_single_val}'), and preceded by a (trivial, no-op) keyboard 'mapping'
   for reference;
 + '{fmt_windows_val}', which shows just the letters visible at the windows;
    and
 + '{fmt_config_val}', which simply shows the specification of the
   configuration (in the same format as {cfg_arg}).
The program is forgiving about forgotten format values and will accept a
range of reasonable substitutes (e.g., {fmt_internal_alts} for
'{fmt_internal_val}').

{hgt_arg} can be used to determine how any encoded-to characters in mappings
(see '{fmt_single_val}' in the note on {fmt_arg}) are highlighted. By default
this highlighting is done with combining Unicode characters, which may not
work on all systems, and as an alternative, any two characters provided as
{hgt_arg} will be used to 'bracket' the highlighted character. To avoid errors,
these characters should be enclosed in quotes.
"""

_EPILOG_ENCODE = _EPILOG_CONFIG + "\n" + _EXAMPLES_ENCODE
_EPILOG_SHOW = _EPILOG_CONFIG + "\n" + _EPILOG_FORMAT + "\n" + _EXAMPLES_SHOW
_EPILOG_RUN = _EPILOG_CONFIG + "\n" + _EPILOG_FORMAT + "\n" + _EXAMPLES_RUN

_EPILOG_ARGS = dict(shw_cmd='show',
                    hgt_arg=_HIGHLIGHT_KWARGS['metavar'],
                    let_arg=_LETTER_KWARGS['metavar'],
                    cfg_arg=_CONFIG_KWARGS['metavar'],
                    fmt_arg=_FORMAT_KWARGS['metavar'],
                    fmt_internal_val=EnigmaConfig._FMTS_INTERNAL[0],
                    fmt_single_val=EnigmaConfig._FMTS_SINGLE[0],
                    fmt_windows_val=EnigmaConfig._FMTS_WINDOWS[0],
                    fmt_config_val=EnigmaConfig._FMTS_CONFIG[0],
                    fmt_internal_alts=' or '.join(["'{}'".format(a) for a in EnigmaConfig._FMTS_INTERNAL[1:]]))
_EPILOG_ENCODE = _EPILOG_ENCODE.format(**_EPILOG_ARGS)
_EPILOG_SHOW = _EPILOG_SHOW.format(**_EPILOG_ARGS)
_EPILOG_RUN = _EPILOG_RUN.format(**_EPILOG_ARGS)

if __name__ == '__main__':

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--verbose', '-v',
                               action='store_true',
                               help='display additional information (may have no effect)')
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

    # Encode a message
    encode_parser = commands.add_parser('encode', parents=[parent_parser], add_help=False,
                                        description=_DESC_ENCODE, epilog=_EPILOG_ENCODE, help=_HELP_ENCODE,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    _CONFIG_KWARGS['help'] = _HELP_ENCODE_CONFIG
    encode_parser.add_argument(*_CONFIG_ARGS, **_CONFIG_KWARGS)
    encode_parser.add_argument(_ENCODE_MESSAGE_ARG, **_ENCODE_MESSAGE_KWARGS)
    encode_display_group = encode_parser.add_argument_group(title='message formatting arguments')
    encode_display_group.add_argument(*_FORMAT_ARGS,
                                      action='store_true',
                                      help='format the encoded message into blocks')
    encode_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # Display machine state
    show_parser = commands.add_parser('show', parents=[parent_parser], add_help=False,
                                      description=_DESC_SHOW, epilog=_EPILOG_SHOW, help=_HELP_SHOW,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    _CONFIG_KWARGS['help'] = _HELP_DSIPLAY_CONFIG
    show_parser.add_argument(*_CONFIG_ARGS, **_CONFIG_KWARGS)
    show_input_group = show_parser.add_argument_group(title='input argument')
    show_input_group.add_argument(*_LETTER_ARGS, **_LETTER_KWARGS)
    show_display_group = show_parser.add_argument_group(**_DISPLAY_GROUP_KWARGS)
    show_display_group.add_argument(*_FORMAT_ARGS, **_FORMAT_KWARGS)
    show_display_group.add_argument(*_HIGHLIGHT_ARGS, **_HIGHLIGHT_KWARGS)
    show_display_group.add_argument(*_SHOWENCODING_ARGS, **_SHOWENCODING_KWARGS)
    show_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

    # Show machine operation
    run_parser = commands.add_parser('run', parents=[parent_parser], add_help=False,
                                     description=_DESC_RUN, epilog=_EPILOG_RUN, help=_HELP_RUN,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    _CONFIG_KWARGS['help'] = _HELP_RUN_CONFIG
    run_parser.add_argument(*_CONFIG_ARGS, **_CONFIG_KWARGS)
    run_input_group = run_parser.add_argument_group(title='input argument')
    run_input_group.add_argument(*_RUN_MESSAGE_ARGS, **_RUN_MESSAGE_KWARGS)
    run_display_group = run_parser.add_argument_group(**_DISPLAY_GROUP_KWARGS)
    run_display_group.add_argument(*_FORMAT_ARGS, **_FORMAT_KWARGS)
    run_display_group.add_argument(*_HIGHLIGHT_ARGS, **_HIGHLIGHT_KWARGS)
    run_display_group.add_argument(*_SHOWENCODING_ARGS, **_SHOWENCODING_KWARGS)
    run_operation_group = run_parser.add_argument_group(title='run operation arguments',
                                                        description='options for controlling stepping and '
                                                                    'annotation of steps')
    # REV - Rework using constands as for others? Revert to not using constants?
    run_operation_group.add_argument('--noinitial', '-n',
                                     action='store_false', dest='initial',
                                     help="don't show the initial starting step")
    run_operation_group.add_argument('--overwrite', '-o',
                                     action='store_true',
                                     help='overwrite each step after a pause '
                                          '(may result in garbled output on some systems)')
    run_operation_group.add_argument('--slower', '-S',
                                     action='count', default=0,
                                     help='slow down overwriting; '
                                          'repeat for more slowing (only has effect with --overwrite)')
    run_operation_group.add_argument('--showstep', '-t', action='store_true',
                                     help='show the step number')
    run_operation_group.add_argument('--steps', '-s',
                                     action='store', metavar=fmt_arg('steps'), nargs='?', default=None, const=1,
                                     type=int,
                                     help='a number of steps to run; if omitted when a message is provided, '
                                          'will default to the length of the message; otherwise defaults to 1')
    run_parser.add_argument(*_HELP_ARGS, **_HELP_KWARGS)

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

            # See 'type' for 'config' and definition of 'unicode_literal' above
            assert isinstance(args.config, unicode), \
                "Unable to decode '{}' to Unicode; report this error!".format(_CONFIG_KWARGS['metavar'])

            cfg = EnigmaConfig.config_enigma_from_string(args.config)
            fmt = args.format

            if args.command == 'encode':
                msg = args.message
                if fmt:
                    cfg.print_encoding(msg)
                else:
                    print(cfg.enigma_encoding(msg))
            else:
                sst = args.command == 'run' and (args.showstep or args.verbose)
                sec = args.showencoding or args.verbose
                mks = (lambda c: args.highlight[0] + c + args.highlight[1]) if args.highlight and len(
                    args.highlight) == 2 else None
                if args.command == 'show':
                    if args.verbose:
                        print(unicode(cfg) + ':\n')
                    let = args.letter
                    print(cfg.config_string(let, fmt, show_encoding=sec, mark_func=mks))
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
