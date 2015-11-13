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

from itertools import cycle, islice
from cachetools import cached

from enigma.utils import *

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FWD = 1
REV = -1


# ASK - How to make private so it can't be instantiated outside of module? Make private to EnigmaConfig? <<<
# TBD - http://stackoverflow.com/a/25041285/656912
class Component(object):
    @property
    def name(self):
        return self._name

    @property
    def wiring(self):
        return self._wiring

    @property
    def turnovers(self):
        return self._turnovers

    def __init__(self, name, wiring, turnovers):

        # REV - Decide what goal to pursue here. What kind of flexibility to allow in creating Components
        assert name not in _comps.keys()

        self._name = name
        self._wiring = wiring
        self._turnovers = turnovers

    # Caching here is essential; see general not on caching.
    @cached({})
    def mapping(self, position, direction=FWD):

        assert direction in [FWD, REV]

        # REV - Smarter handling of edge cases and bounds?
        def rot_map(mp, st):
            st %= 26
            return list(islice(cycle(mp), st, 26 + st))

        steps = position - 1

        # REV - Use list comprehensions instead of map?
        if direction == REV:
            # return ''.join(map(chr_A0, ordering(self.mapping(position, FWD))))
            return ''.join([chr_A0(p) for p in ordering(self.mapping(position, FWD))])
        else:
            # return ''.join(map(lambda ch: rot_map(LETTERS, -steps)[num_A0(ch)], rot_map(self._wiring, steps)))
            return ''.join([rot_map(LETTERS, -steps)[num_A0(c)] for c in rot_map(self._wiring, steps)])

    def __unicode__(self):
        return "{0} {1} {2}".format(self._name, self._wiring, self._turnovers)

    def __str__(self):
        return unicode(self).encode('utf-8')


# REV - Better way to initialize and store these as constants? <<<
_comps = dict()

_rots = dict()
_comps['I'] = _rots['I'] = Component('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
_comps['II'] = _rots['II'] = Component('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
_comps['III'] = _rots['III'] = Component('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')
_comps['IV'] = _rots['IV'] = Component('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
_comps['V'] = _rots['V'] = Component('V', 'VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
_comps['VI'] = _rots['VI'] = Component('VI', 'JPGVOUMFYQBENHZRDKASXLICTW', 'ZM')
_comps['VII'] = _rots['VII'] = Component('VII', 'NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM')
_comps['VIII'] = _rots['VIII'] = Component('VIII', 'FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM')
_comps['β'] = _rots['β'] = Component('β', 'LEYJVCNIXWPBQMDRTAKZGFUHOS', '')
_comps['γ'] = _rots['γ'] = Component('γ', 'FSOKANUERHMBTIYCWLQPZXVGJD', '')

_refs = dict()
_comps['A'] = _refs['A'] = Component('A', 'EJMZALYXVBWFCRQUONTSPIKHGD', '')
_comps['B'] = _refs['B'] = Component('B', 'YRUHQSLDPXNGOKMIEBFZCWVJAT', '')
_comps['C'] = _refs['C'] = Component('C', 'FVPJIAOYEDRZXWGCTKUQSBNMHL', '')
_comps['b'] = _refs['b'] = Component('b', 'ENKQAUYWJICOPBLMDXZVFTHRGS', '')
_comps['c'] = _refs['c'] = Component('c', 'RDOBJNTKVEHMLFCWZAXGYIPSUQ', '')

_kbd = dict()
_comps[''] = _kbd[''] = Component('', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '')

rotors = sorted(_rots.keys())
reflectors = sorted(_refs.keys())


def component(name):
    def plug(letters, swap):
        if len(swap) == 2 and swap[0] in LETTERS and swap[1] in letters:
            # return map(lambda ch: swap[0] if ch == swap[1] else (swap[1] if ch == swap[0] else ch), letters)
            return [swap[0] if c == swap[1] else swap[1] if c == swap[0] else c for c in letters]
        else:
            return letters

    if name not in _comps.keys():
        _comps[name] = Component(name, ''.join(reduce(plug, name.split('.'), list(LETTERS))), '')
    return _comps[name]