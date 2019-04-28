#!/usr/bin/env python
# encoding: utf8
#from __future__ import (absolute_import, print_function, division, unicode_literals)

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
    assert 'EKMFLGDQVZNTOWYHXUSPAIBRCJ' == component('I').mapping(1, Direction.FWD)
    assert 'QGCLFMUKTWZDNJYVOESIBPRAHX' == component('II').mapping(-1, Direction.FWD)
    assert 'CEGIKBOQSWUYMXDHVFZJLTRPNA' == component('III').mapping(2, Direction.FWD)
    assert 'PZEHVRYSCMDBTXLUKAOQIWJNGF' == component('IV').mapping(-2, Direction.FWD)

    assert 'RVHKXCSFBUMPJWNEGZYDIQOTLA' == component('VIII').mapping(11, Direction.REV)
    assert 'XZVROSMPJIWNGLEHUDFYQCKATB' == component('B').mapping(-12, Direction.REV)
    assert 'DUEACLXWRVPFZTSKYIONBJHGQM' == component('C').mapping(17, Direction.REV)
    assert 'MTPRJAYQKZLHUGFNWOCIXBVESD' == component('V').mapping(-8, Direction.REV)

    for r in rotors + reflectors:
        assert component(r).wiring == component(r).mapping(1, Direction.FWD)


def test_component_string():
    # Components as strings
    assert 'c-γ-I-VIII-III UYZO UX.MI 03.22.04.09' == str(
        EnigmaConfig.config_enigma('c-γ-I-VIII-III', 'UYZO', 'UX.MI', '03.22.04.09'))
    assert 'b-β-I-II-III AAAA UX.LU.QW.MI 01.11.14.04' == str(
        EnigmaConfig.config_enigma('b-β-I-II-III', 'AAAA', 'UX.LU.QW.MI', '01.11.14.04'))


def test_component_equality():
    args_a = ['c-γ-I-VIII-III', 'UYZO', 'UX.MI', '03.22.04.09']
    args_b = ['c-γ-I-VIII-III', 'UYZO', 'UX.MI', '03.22.04.09']
    cfg_a = EnigmaConfig.config_enigma(*args_a)
    cfg_b = EnigmaConfig.config_enigma(*args_b)
    assert cfg_a == cfg_b
    assert cfg_a.step() == cfg_b.step()
    assert cfg_a == EnigmaConfig(cfg_b.components, cfg_b.positions, cfg_b.rings)
    assert cfg_b == EnigmaConfig(cfg_b.components, cfg_b.positions, cfg_b.rings)
    assert cfg_a == EnigmaConfig(cfg_a.components, cfg_a.positions, cfg_a.rings)
    assert cfg_b == EnigmaConfig.config_enigma_from_string(' '.join(args_b))
    assert cfg_b == EnigmaConfig.config_enigma_from_string(' '.join(args_a))


def test_component_validity():
    with pytest.raises(EnigmaValueError) as e:
        cmp = Component('y', 'PQR', 'Q')
    with pytest.raises(AssertionError) as e:
        cmp = Component('I', 'PQR', 'Q')