#!/usr/bin/env python
# encoding: utf8
#from __future__ import (absolute_import, print_function, division, unicode_literals)

''' Simple test file for debugging and testing at the shell. To use simply
        python test.py
    or
        ./test.py
    or run 'test' in PyCharm.
'''

import pytest

from crypto_enigma.machine import *

# Test utilities and internals

def test_encoding_chars():
    with pytest.raises(EnigmaValueError) as e:
        mpg = Mapping("PQR")
    # assert Mapping("PQR").encode_char('Z') == ' '
    # assert Mapping("PQR").encode_char('B') == 'Q'
    # assert Mapping("").encode_char(' ') == ' '

# TBD - Replace <<<
def test_marked_mapping():
    pass
    # for s in [Mapping("AMC"), Mapping("ANNCJDDJSJKKWKWK"), Mapping(""), Mapping("dkjfsldfjhsljdhflskjdfh")]:
    #     assert EnigmaConfig._marked_mapping(s, 50) == s

# TBD - Replace <<<
def test_locate_letter():
    pass
    # for s in [Mapping("AMC"), Mapping("ANNCJDDJSJKKWKWK"), Mapping("A"), Mapping("dkjfslAdfjhsljdhflskjdfh")]:
    #     assert EnigmaConfig._locate_letter(s, 'A', "zzzzz") == -1
    # for s in [Mapping("AMC"), Mapping("ANNCJDDJSJKKWKWK"), Mapping("A"), Mapping("dkjfslAdfjhsljdhflskjdfh")]:
    #     assert EnigmaConfig._locate_letter(s, '5', "zzzzz") == -1

# TBD - Replace <<<
def test_make_message():
    pass
    # assert EnigmaConfig.make_message("AHDuRIWDHUWYRdDUSHSBBqDyXJ") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"
    # assert EnigmaConfig.make_message("AHDuRI WDHUWYR dDUSHS BBqDyXJ") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"
    # assert EnigmaConfig.make_message("AγH*D+uRI WDHβUγWYR dDβ*USHS BBγqDyXJ") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"
    # assert EnigmaConfig.make_message("AγH*D+uRI WDHβUγWYR dDβ*USHS BBγqDyXJ") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"
    # assert EnigmaConfig.make_message("AγH*D+uRI WDHβUγWYR dDβ*USHS BBγqDy!'") == "AHDURIWDHUWYRDDUSHSBBQDYXJ"