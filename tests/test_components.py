#!/usr/bin/env python
# encoding: utf8
from __future__ import (absolute_import, print_function, division, unicode_literals)

''' Simple test file for debugging and testing at the shell. To use simply
        python test.py
    or
        ./test.py
    or run 'test' in PyCharm.
'''

from crypto_enigma.machine import *
from crypto_enigma.components import _comps

# Comparing output with output generated from Haskell version
# USE - Replace greek letters in Haskell-generated output

def test_component_keys():
    # Component names
    assert rotors == sorted(['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'β', 'γ'])
    assert reflectors == sorted(['A', 'B', 'C', 'b', 'c'])

    for r in rotors + reflectors:
        assert component(r) == _comps[r]

def test_component_rotation():
    # Component rotation
    assert 'EKMFLGDQVZNTOWYHXUSPAIBRCJ' == component('I').mapping(1, FWD)
    assert 'QGCLFMUKTWZDNJYVOESIBPRAHX' == component('II').mapping(-1, FWD)
    assert 'CEGIKBOQSWUYMXDHVFZJLTRPNA' == component('III').mapping(2, FWD)
    assert 'PZEHVRYSCMDBTXLUKAOQIWJNGF' == component('IV').mapping(-2, FWD)

    assert 'RVHKXCSFBUMPJWNEGZYDIQOTLA' == component('VIII').mapping(11, REV)
    assert 'XZVROSMPJIWNGLEHUDFYQCKATB' == component('B').mapping(-12, REV)
    assert 'DUEACLXWRVPFZTSKYIONBJHGQM' == component('C').mapping(17, REV)
    assert 'MTPRJAYQKZLHUGFNWOCIXBVESD' == component('V').mapping(-8, REV)

    for r in rotors + reflectors:
        assert component(r).wiring == component(r).mapping(1, FWD)


def test_component_string():
    # Components as strings
    assert 'c-γ-I-VIII-III UYZO UX.MI 03.22.04.09' == unicode(
        EnigmaConfig.config_enigma('c-γ-I-VIII-III', 'UYZO', 'UX.MI', '03.22.04.09'))
    assert 'b-β-I-II-III AAAA UX.LU.QW.MI 01.11.14.04' == unicode(
        EnigmaConfig.config_enigma('b-β-I-II-III', 'AAAA', 'UX.LU.QW.MI', '01.11.14.04'))
