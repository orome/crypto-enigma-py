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

    # TBD - Replace with new tests for valid argument types? <<<

    # try:
    #     cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', '03.17.04.11')
    #     assert False
    # except TypeError as e:
    #     assert e.message == "Parameter 'rotor_names' should be Unicode"
    # try:
    #     cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', b'LFAQ', '', '03.17.04.11')
    #     assert False
    # except TypeError as e:
    #     assert "Parameter 'window_letters' should be Unicode" in str(e)
    # try:
    #     cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', b'03.17.04.11')
    #     assert False
    # except TypeError as e:
    #     assert "Parameter 'rings' should be Unicode" in str(e)

    # REV - Alternate method - http://stackoverflow.com/a/33920418/656912
    # with pytest.raises(TypeError) as e:
    #     cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', '03.17.04.11')
    # assert "Parameter 'rotor_names' should be Unicode" in str(e)
    # with pytest.raises(TypeError) as e:
    #     cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', b'03.17.04.11')
    # assert "Parameter 'rings' should be Unicode" in str(e)
    # with pytest.raises(TypeError) as e:
    #     cfg = EnigmaConfig.config_enigma('b-γ-V-VIII-II', 'LFAQ', '', '03.17.04.11')
    #     cfg.enigma_encoding(b'XYZ')
    # assert "Parameter 'message' should be Unicode" in str(e)
