#!/usr/bin/env python
# encoding: utf8

""" 
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)
import warnings

from itertools import cycle, islice

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FWD = 1
REV = -1


def num_A0(c):
    return ord(c) - ord('A')

#
# num_A0 = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10,
#           'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21,
#           'W': 22, 'X': 23, 'Y': 24, 'Z': 25, ' ': -33}


def chr_A0(n):
    return chr(n + ord('A'))


def ordering(items):
    return [i[1] for i in sorted(zip(items,range(0,len(items))))]


# standard simple-substitution cypher encoding
def encode_char(mapping, ch):
    if ch == ' ':
        return ' '
    else:
        return mapping[num_A0(ch)]

def encode_num(mapping, num):
    if num == -33:
        return -33
    else:
        return mapping[num]

def encode_string(mapping, string):
        return ''.join([encode_char(mapping, ch) for ch in string])

def encode_nums(mapping, nums):
        return ''.join([encode_num(mapping, num) for num in nums])




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
        # Some ugly caching; see mapping()
        self.__cached_mappings = dict()
        self.__cached_mappings[FWD] = dict()
        self.__cached_mappings[REV] = dict()

    def mapping(self, position, direction=FWD):

        assert direction in [FWD,REV]

        # REV - Smarter handling of edge cases and bounds?
        def rot_map(mp, st):
            st %= 26
            return list(islice(cycle(mp), st, 26+st))

        if position not in self.__cached_mappings[direction].keys():

            steps = position - 1

            # REV - Use list comprehensions instead of map?
            # Some ugly caching, since upper rotors change slowly and coputing mappings is time consuming
            # TBD - Make less ugly by trapping inexing?
            if direction == REV:
                self.__cached_mappings[REV][position] = ''.join(map(chr_A0, ordering(self.mapping(position, FWD))))
            else:
                self.__cached_mappings[FWD][position] = ''.join(map(lambda ch: rot_map(LETTERS, -steps)[num_A0(ch)], rot_map(self._wiring, steps)))

        return  self.__cached_mappings[direction][position]


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

    def plug(letters, swap):
        if len(swap) == 2 and swap[0] in LETTERS and swap[1] in letters:
            return map(lambda ch: swap[0] if ch == swap[1] else (swap[1] if ch == swap[0] else ch), letters)
        else:
            return letters

    if name not in _comps.keys():
        _comps[name] = Component(name, ''.join(reduce(plug, name.split('.'), list(LETTERS))), '')
    return _comps[name]


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

    # REV - Possibly not needed (also possibly not needed in Haskell? Used for printing though.)
    @property
    def stages(self):
        return self._stages

    # TBD - Make private somehow? <<<
    def __init__(self, components, positions, rings):
        self._components = tuple(components)
        self._positions = tuple(positions)
        self._rings = tuple(rings)
        self._stages = tuple(range(0,len(self._components)))

    @staticmethod
    def config_enigma(rotor_names, window_letters, plugs, rings):

        comps = list(reversed((rotor_names+'-'+plugs).split('-')))
        winds = list(reversed([num_A0(c) for c in 'A'+window_letters+'A']))
        rngs = list(reversed([int(x) for x in ('01.'+rings+'.01').split('.')]))

        # TBD - Assertions for validation; plugboard <<<
        assert all(name in rotors for name in comps[1:-1])
        assert comps[-1] in reflectors
        assert len(rngs) == len(winds) == len(comps)
        assert all(1 <= rng <= 26 for rng in rngs)
        assert all(chr_A0(wind) in LETTERS for wind in winds)

        return EnigmaConfig(comps, map(lambda w, r: ((w - r + 1) % 26) + 1, winds, rngs), rngs)

    def _window_letter(self, st):
        return chr_A0((self._positions[st] + self._rings[st] - 2) % 26)

    def windows(self):
        return ''.join(list(reversed([self._window_letter(st) for st in self._stages][1:-1])))

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

        stepped_positions = [((self._positions[stage] + pos_inc(stage) - 1) % 26) + 1 for stage in self._stages]

        return EnigmaConfig(self._components, stepped_positions, self._rings)

    def stepped_configs(self, steps=None):
        cur_config = self
        cur_step = 0
        while steps is None or cur_step <= steps:
            if cur_step > 0:
                cur_config = cur_config.step()
            yield cur_config
            cur_step += 1

    def stage_mapping_list(self):

        return ([component(comp).mapping(pos, FWD) for (comp, pos) in zip(self._components, self._positions)] +
                [component(comp).mapping(pos, REV) for (comp, pos) in reversed(zip(self._components, self._positions)[:-1])])

    # TBD - Maybe not needed; no scan in Python -- see http://stackoverflow.com/a/24503765/656912 <<<
    def enigma_mapping_list(self):
        """
        .. deprecated:: 0.00.001
           This function unused in this implementation.
           See the `Haskall version <https://hackage.haskell.org/package/crypto-enigma/docs/Crypto-Enigma.html#v:stageMappingList>`_ of this package, where it is.
        """
        warnings.warn("Function 'enigma_mapping_list' is not implemented.", DeprecationWarning)
        #raise NotImplementedError

    # REV - Just last of enigma_mapping_list() if implemented
    def enigma_mapping(self):
        return reduce(lambda string, mapping: encode_string(mapping, string), self.stage_mapping_list(), LETTERS)

    def enigma_encoding(self, message):

        assert  all(letter in LETTERS for letter in message)

        return ''.join([encode_char(step_config.enigma_mapping(), letter) for
                        (letter, step_config) in zip(message, self.step().stepped_configs())])

    # ASK - Equvalent to Haskell read (if this is like show, or is _repr_ show; eval(repr(obj)) )? <<<
    def __unicode__(self):
        return "{0} {1} {2} {3}".format('-'.join(reversed(self._components[1:])),
                                        self.windows(),
                                        self._components[0],
                                        '.'.join(reversed(['{:02d}'.format(r) for r in self._rings[1:-1]])))

    def __str__(self):
        return unicode(self).encode('utf-8')