#!/usr/bin/env python
# encoding: utf8

""" 
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)

from itertools import cycle, islice

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FWD = 1
REV = -1


def num_A0(c):
    return ord(c) - ord('A')


def chr_A0(n):
    return chr(n + ord('A'))


def ordering(items):
    return [i[1] for i in sorted(zip(items,range(0,len(items))))]


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

    # REV - Use lists rather than strings (strings only for display)? See how much conversion happens.
    def __init__(self, name, wiring, turnovers):

        # TBD - Decide what design goal to pursue here; thos won't map directly to Haskell (http://stackoverflow.com/a/25041285/656912)
        assert name not in _comps.keys()

        self._name = name
        self._wiring = wiring
        self._turnovers = turnovers

    def mapping(self, position, direction=FWD):

        assert direction in [FWD,REV]

        # REV - Smarter handling of edge cases and bounds?
        def rot_map(mp, st):
            st %= 26
            return list(islice(cycle(mp), st, 26+st))

        steps = position - 1

        # REV - Use list comprehensions instead of map?
        if direction == REV:
            return ''.join(map(chr_A0, ordering(self.mapping(position, FWD))))
        else:
            return ''.join(map(lambda ch: rot_map(LETTERS, -steps)[num_A0(ch)], rot_map(self.wiring, steps)))


# REV - Better way to initialize and store these as constants? <<<
_comps = dict()

_rots = dict()
_comps['I'] = _rots['I'] = Component('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ','Q')
_comps['II'] = _rots['II'] = Component('II','AJDKSIRUXBLHWTMCQGZNPYFVOE','E')
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

rotors = _rots.keys()
reflectors = _refs.keys()

def component(name):
    if name in _comps.keys():
        return _comps[name]
    else:
        # TBD - Generate wiring for plugboard <<<
        _comps[name] = Component(name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '')


class EnigmaConfig(object):

    @property
    def components(self):
        return self._components

    @property
    def positions(self):
        return self._positions

    @property
    def rings(self):
        return self._rings

    @property
    def stages(self):
        return self._stages

    # TBD - Make this configEnigma and replace this with direct consructor (for use in step?)
    def __init__(self, rotor_names, window_letters, plugs, rings):

        comps = list(reversed((rotor_names+'-'+plugs).split('-')))
        winds = list(reversed([num_A0(c) for c in 'A'+window_letters+'A']))
        rngs = list(reversed([int(x) for x in ('01.'+rings+'.01').split('.')]))

        # TBD - Assertions for validation; plugboard <<<
        assert all(name in rotors for name in comps[1:-1])
        assert comps[-1] in reflectors
        assert len(rngs) == len(winds) == len(comps)
        assert all(1 <= rng <= 26 for rng in rngs)
        assert all(chr_A0(wind) in LETTERS for wind in winds)

        self._components = comps
        self._positions = map(lambda w, r: ((w - r + 1) % 26) + 1, winds, rngs)
        self._rings = rngs
        self._stages = range(0,len(self._components))

    def _window_letter(self, st):
        return chr_A0((self._positions[st] + self._rings[st] - 2) % 26)

    def windows(self):
        return ''.join(list(reversed([self._window_letter(st) for st in self._stages][1:-1])))

    # TBD - Should be something I can do with iterators here (use step to implement next?) <<<
    # TBD - Decide on best strategy for iteration and on whether EnigmaConfig should be mutable (or step returns new) <<<
    def step(self):

        def is_turn(stg):
            return self._window_letter(stg) in component(self.components[stg]).turnovers

        def pos_inc(stg):
            if stg == 0:
                return 0
            elif stg > 3:
                return 0
            elif stg == 1:
                return 1
            elif stg == 2 and is_turn(2):
                return 1
            elif is_turn(stg-1):
                return 1
            else:
                return 0

        self._positions = [((self._positions[stage] + pos_inc(stage) - 1) % 26) + 1 for stage in self.stages]
        return self

    def stepped_configs(self, steps):
        cur_step = 0
        while cur_step <= steps:
            if cur_step == 0:
                yield self
            else:
                yield self.step()
            cur_step += 1
