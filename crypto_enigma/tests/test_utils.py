#!/usr/bin/env python
# encoding: utf8
from __future__ import (absolute_import, print_function, division, unicode_literals)

''' Simple test file for debugging and testing at the shell. To use simply
        python test.py
    or
        ./test.py
    or run 'test' in PyCharm.
'''

from ..machine import *

# Test utilities and internals

def test_encoding_chars():
    assert encode_char("PQR", 'Z') == ' '
    assert encode_char("PQR", 'B') == 'Q'
    assert encode_char("", ' ') == ' '


def test_marked_mapping():
    for s in ["AMC", "ANNCJDDJSJKKWKWK", "", "dkjfsldfjhsljdhflskjdfh"]:
        assert EnigmaConfig._marked_mapping(s, 50) == s


def test_locate_letter():
    for s in ["AMC", "ANNCJDDJSJKKWKWK", "A", "dkjfslAdfjhsljdhflskjdfh"]:
        assert EnigmaConfig._locate_letter(s, 'A', "zzzzz") == -1
    for s in ["AMC", "ANNCJDDJSJKKWKWK", "A", "dkjfslAdfjhsljdhflskjdfh"]:
        assert EnigmaConfig._locate_letter(s, '5', "zzzzz") == -1


def test_make_message():
    assert EnigmaConfig.make_message("AHDuRIWDHUWYRdDUSHSBBqDyXJ") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"
    assert EnigmaConfig.make_message("AHDuRI WDHUWYR dDUSHS BBqDyXJ") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"
    assert EnigmaConfig.make_message("AγH*D+uRI WDHβUγWYR dDβ*USHS BBγqDyXJ") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"
    assert EnigmaConfig.make_message("AγH*D+uRI WDHβUγWYR dDβ*USHS BBγqDyXJ") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"
    assert EnigmaConfig.make_message("AγH*D+uRI WDHβUγWYR dDβ*USHS BBγqDy!'") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"