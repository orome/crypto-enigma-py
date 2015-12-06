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

from .utils import *

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FWD = 1
REV = -1


class Mapping(unicode):

    def __init__(self, str):
        super(Mapping, self).__init__()
        self._len = len(self)

    # standard simple-substitution cypher encoding
    def encode_char(self, ch):
        if 0 <= num_A0(ch) < self._len:
            return self[num_A0(ch)]
        else:
            return ' '

    def encode_string(self, string):
        return ''.join([self.encode_char(ch) for ch in string])


# ASK - How to make private so it can't be instantiated outside of module? Make private to EnigmaConfig? <<<
# TBD - http://stackoverflow.com/a/25041285/656912
class Component(object):

    def __init__(self, name, wiring, turnovers):

        # REV - Decide what goal to pursue here. What kind of flexibility to allow in creating Components
        assert name not in _comps.keys()

        self._name = name
        self._wiring = Mapping(wiring)
        self._turnovers = turnovers

    @property
    def name(self):
        """The name identifying a component of an Enigma machine.

        For rotors (including the reflector) this is one of the conventional letter or Roman numeral designations
        (e.g., `'IV'` or `'β'`).
        For the plugboard this is the conventional string of letter pairs, indicating letters wired together
        by plugging (e.g., `'AU.ZM.ZL.RQ'`). Absence or non-use of a plugboard can be indicated with `'~'`
        (or almost anything that isn't a valid plugboard spec).

        Returns:
            unicode: A string uniquely specifying a `Component`.

        """
        return self._name

    @property
    def wiring(self):
        """The physical wiring of a component, expressed as a |mapping|.

        Returns:
            Mapping: The `mapping` established by the physical wiring of a `Component`:
                the forward mapping when **01** is at the window position for rotors;
                by the plug arrangement for the plugboard.

        Examples:
            A rotor's wiring is fixed by the physical connections of the wires inside the roter:

            >>> cmp = component('V')
            >>> cmp.wiring
            u'VZBRGITYUPSDNHLXAWMJQOFECK'

            For plugboards, it is established by the specified connections:

            >>> component('AZ.BY').wiring
            u'ZYCDEFGHIJKLMNOPQRSTUVWXBA'

        """
        return self._wiring

    @property
    def turnovers(self):
        """The turnover positions for a rotor.

        Returns:
            unicode: The letters on a rotor's ring that appear at the window (see `~.machine.EnigmaConfig.windows`)
                when the ring is in the turnover position.
                Not applicable (and empty) for the plugboard and for reflectors.
                (See `.machine.EnigmaConfig.step`.)

        """
        return self._turnovers

    # Caching here is essential; see general not on caching.
    @cached({})
    def mapping(self, position, direction=FWD):
        """The mapping performed by a component based on its rotational position.

        The |mapping| performed by a `Component` as a function of its position (see `~.machine.EnigmaConfig.positions`)
        in an Enigma machine and the direction of the signal passing through it.

        For all other positions of rotors, the mapping is a cyclic permutation this wiring's inputs (backward)
        and outputs (forward) by the rotational offset of the rotor away from the **01** position.

        Args:
            position (int): The rotational offset of the `Component` in the Enigma machine.
            direction: The direction of signal passage through the component.

        Returns:
            Mapping: The |mapping| performed by the component in the `direction` when `position` is
                at the window position.

        Examples:
            Note that because the wiring of reflectors generates mappings that consist entirely of paired exchanges
            of letters, reflectors (at any position) produce the same mapping in both directions (the same is true
            of the plugboard):

            >>> all(c.mapping(p, FWD) == c.mapping(p, REV) for c in map(component, reflectors) for p in range(1,26))
            True

        For rotors in their base position, with **01** at the window position, and for the plugboard,
        this is just the `wiring`:

        >>> cmp.wiring == cmp.mapping(1, FWD)
        True

        """

        assert direction in [FWD, REV]

        # REV - Smarter handling of edge cases and bounds?
        def rot_map(mp, st):
            st %= 26
            return list(islice(cycle(mp), st, 26 + st))

        steps = position - 1

        # REV - Use list comprehensions instead of map?
        if direction == REV:
            # return ''.join(map(chr_A0, ordering(self.mapping(position, FWD))))
            return Mapping(''.join([chr_A0(p) for p in ordering(self.mapping(position, FWD))]))
        else:
            # return ''.join(map(lambda ch: rot_map(LETTERS, -steps)[num_A0(ch)], rot_map(self._wiring, steps)))
            return Mapping(''.join([rot_map(LETTERS, -steps)[num_A0(c)] for c in rot_map(self._wiring, steps)]))

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


@require_unicode('name')
def component(name):
    def plug(letters, swap):
        if len(swap) == 2 and swap[0] in LETTERS and swap[1] in letters:
            # return map(lambda ch: swap[0] if ch == swap[1] else (swap[1] if ch == swap[0] else ch), letters)
            return [swap[0] if c == swap[1] else swap[1] if c == swap[0] else c for c in letters]
        else:
            return letters

    if name not in _comps.keys():
        _comps[name] = Component(name, ''.join(reduce(plug, name.split('.'), list(LETTERS))), '')
    assert sorted(_comps[name].wiring) == list(LETTERS)
    assert all([t in _comps[name].wiring for t in _comps[name].turnovers])
    return _comps[name]