#!/usr/bin/env python
# encoding: utf8
from __future__ import (absolute_import, print_function, division, unicode_literals)

''' Simple test file for debugging and testing at the shell. To use simply
        python test.py
    or
        ./test.py
    or run 'test' in PyCharm.
'''
import pytest

from crypto_enigma.machine import *


# Tests of expected exceotpions from providing non-unicode arguments

# ASK - How to test for expected exceptions (and their values) <<<
# TBD - Expand tests <<<
def test_config_unicode():
    # EnigmaConfig arguments
    try:
        cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', '03.17.04.11')
        assert True
    except TypeError as e:
        assert False
    try:
        cfg = EnigmaConfig.config_enigma(b'b-γ-V-VIII-II', 'LFAQ', '', '03.17.04.11')
        assert False
    except TypeError as e:
        assert e.message == "Parameter 'rotor_names' should be Unicode"
    try:
        cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', b'LFAQ', '', '03.17.04.11')
        assert False
    except TypeError as e:
        assert e.message == "Parameter 'window_letters' should be Unicode"
    try:
        cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', b'03.17.04.11')
        assert False
    except TypeError as e:
        assert e.message == "Parameter 'rings' should be Unicode"

    # REV - Alternate method - http://stackoverflow.com/a/33920418/656912
    with pytest.raises(TypeError) as e:
        cfg = EnigmaConfig.config_enigma(b'b-γ-V-VIII-II', 'LFAQ', '', '03.17.04.11')
    assert e.value.message == "Parameter 'rotor_names' should be Unicode"
    with pytest.raises(TypeError) as e:
        cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', b'03.17.04.11')
    assert e.value.message == "Parameter 'rings' should be Unicode"
    with pytest.raises(TypeError) as e:
        cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', '03.17.04.11')
        cfg.enigma_encoding(b'XYZ')
    assert e.value.message == "Parameter 'message' should be Unicode"
