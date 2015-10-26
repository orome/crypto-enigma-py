#!/usr/bin/env python
# encoding: utf8

""" 
Description

.. note::
    Any additional note.
"""

# TBD - Changer list(reverse( conversions to [::-1] throughout <<<
# REV - Additional performance improvements
# A large speed improvement comes from caching the encodings of rotors when first computed for a given position.
# This is effective because upper rotors don't change frequently so such cached mappings are reused many times. And
# because even the lower rotors will assume a maximum of 26 distinct positions, the cache will always be small.
# Improvements from implementing mappings as lists of numbers rather than strings are negligible and not worth the loss
# of clarity.
from __future__ import (absolute_import, print_function, division, unicode_literals)

from cachetools import cached
from itertools import cycle, islice

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FWD = 1
REV = -1


def num_A0(c):
    return ord(c) - ord('A')


def chr_A0(n):
    return chr(n + ord('A'))


def ordering(items):
    return [i[1] for i in sorted(zip(items, range(0, len(items))))]


# standard simple-substitution cypher encoding
def encode_char(mapping, ch):
    if ch == ' ':
        return ' '
    else:
        return mapping[num_A0(ch)]


def encode_string(mapping, string):
    return ''.join([encode_char(mapping, ch) for ch in string])

# scan, becaus it's missing from Python; implemented to anticipate Python 3
def accumulate(l, f):
    it = iter(l)
    total = next(it)
    yield total
    for element in it:
        total = f(total, element)
        yield total


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

        # REV - Decide what goal to prusue here. What kind of flexibility to allow in creating Components
        assert name not in _comps.keys()

        self._name = name
        self._wiring = wiring
        self._turnovers = turnovers

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
            #return ''.join(map(chr_A0, ordering(self.mapping(position, FWD))))
            return ''.join([chr_A0(p) for p in ordering(self.mapping(position, FWD))])
        else:
            #return ''.join(map(lambda ch: rot_map(LETTERS, -steps)[num_A0(ch)], rot_map(self._wiring, steps)))
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

rotors = _rots.keys()
reflectors = _refs.keys()


def component(name):
    def plug(letters, swap):
        if len(swap) == 2 and swap[0] in LETTERS and swap[1] in letters:
            #return map(lambda ch: swap[0] if ch == swap[1] else (swap[1] if ch == swap[0] else ch), letters)
            return [swap[0] if c == swap[1] else swap[1] if c == swap[0] else c for c in letters]
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

    # REV - Not used here except for display; possibly not needed in Haskell version either?
    @property
    def stages(self):
        return self._stages

    # TBD - Make private somehow? <<<
    def __init__(self, components, positions, rings):
        self._components = tuple(components)
        self._positions = tuple(positions)
        self._rings = tuple(rings)
        self._stages = tuple(range(0, len(self._components)))

    @staticmethod
    def config_enigma(rotor_names, window_letters, plugs, rings):

        comps = list(reversed((rotor_names + '-' + plugs).split('-')))
        winds = list(reversed([num_A0(c) for c in 'A' + window_letters + 'A']))
        rngs = list(reversed([int(x) for x in ('01.' + rings + '.01').split('.')]))

        # TBD - Assertions for validation; plugboard <<<
        assert all(name in rotors for name in comps[1:-1])
        assert comps[-1] in reflectors
        assert len(rngs) == len(winds) == len(comps)
        assert all(1 <= rng <= 26 for rng in rngs)
        assert all(chr_A0(wind) in LETTERS for wind in winds)

        #return EnigmaConfig(comps, map(lambda w, r: ((w - r + 1) % 26) + 1, winds, rngs), rngs)
        return EnigmaConfig(comps, [((w - r + 1) % 26) + 1 for w, r in zip(winds, rngs)], rngs)

    def _window_letter(self, st):
        return chr_A0((self._positions[st] + self._rings[st] - 2) % 26)

    def windows(self):
        return ''.join(list(reversed([self._window_letter(st) for st in self._stages][1:-1])))
        #return ''.join([self._window_letter(st) for st in self._stages][-1:1:-1])

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
            elif is_turn(stg - 1):
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

    @cached({})
    def stage_mapping_list(self):
            return ([component(comp).mapping(pos, FWD) for (comp, pos) in
                     zip(self._components, self._positions)] +
                    [component(comp).mapping(pos, REV) for (comp, pos) in
                     reversed(zip(self._components, self._positions)[:-1])])

    @cached({})
    def enigma_mapping_list(self):
            return list(accumulate(self.stage_mapping_list(), lambda s, m: encode_string(m, s)))


    def enigma_mapping(self):
        #return reduce(lambda string, mapping: encode_string(mapping, string), self.stage_mapping_list(), LETTERS)
        return self.enigma_mapping_list()[-1]

    def enigma_encoding(self, message):

        assert all(letter in LETTERS for letter in message)

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

    @staticmethod
    def _marked_mapping(mapping, i, marked_char=lambda c: c + '\u0332\u0305'):

        return mapping[:i] + marked_char(mapping[i]) + mapping[i+1:] if 0 <= i <= 25 else mapping

    @staticmethod
    def _locate_letter(mapping, letter, string):
        #locate the index of the encoding with mapping of letter, in string
        return string.index(encode_char(mapping, letter)) if letter in string else -1

    def config_string(self, letter):

        cfg_mapping = self.enigma_mapping()

        return '{0} {1}  {2}  {3}'.format(letter + ' >' if letter in LETTERS else '   ',
                                          EnigmaConfig._marked_mapping(cfg_mapping,
                                                                       EnigmaConfig._locate_letter(cfg_mapping,
                                                                                                   letter,
                                                                                                   cfg_mapping)),
                                          self.windows(),
                                          ' '.join(['{:02d}'.format(p) for p in reversed(self.positions[1:-1])]))

    def config_string_internal(self, letter):

        cfg_mapping = self.enigma_mapping()
        cfg_mapping_list = self.enigma_mapping_list()
        stg_mapping_list = self.stage_mapping_list()

        def reflect_info(stg_info): return stg_info + stg_info[::-1][1:]

        def pad_info(stg_info, pad): return [pad] + stg_info + ([pad] * len(self.positions))

        # REV - Better way that avoids recalcs of cfg_mapping and cfg_mapping_list?
        letter_locations = [EnigmaConfig._locate_letter(m, l, s) for (m, l, s) in
                            zip([LETTERS] + cfg_mapping_list + [cfg_mapping],
                                [letter] * (len(self.stages)*2+1),
                                [LETTERS] + stg_mapping_list + [cfg_mapping])]

        stg_labels = reflect_info(['P'] + list(self.stages)[1:-1] + ['R'])
        stg_mappings = [EnigmaConfig._marked_mapping(m, i) for (m, i) in zip(stg_mapping_list,
                                                                             letter_locations[1:-1])]
        stg_windows = pad_info(list(self.windows())[::-1], ' ')
        stg_positions = pad_info(['{:02d}'.format(p) for p in self.positions][1:-1], '  ')
        stg_coponents = reflect_info(self.components)

        return ("{0}  {1}\n".format(letter + ' >' if letter in LETTERS else '   ',
                                    EnigmaConfig._marked_mapping(LETTERS,letter_locations[1])) +
                ''.join(['  {0}  {1}  {2}  {3}  {4}\n'.format(stg_lbl, stg_map, stg_wind, stg_pos, stg_comp)
                         for (stg_lbl, stg_map, stg_wind, stg_pos, stg_comp) in zip(stg_labels,
                                                                                    stg_mappings,
                                                                                    stg_windows,
                                                                                    stg_positions,
                                                                                    stg_coponents)]) +
                "{0}  {1}".format(encode_char(self.enigma_mapping(), letter) + ' <' if letter in LETTERS else '   ',
                                  EnigmaConfig._marked_mapping(cfg_mapping, letter_locations[-1]))
                )

    # ASK - How to pass a method that may use differnet instances?
    # def _print_operation(self, message, configstring=_config_string):
    #     for (cfg, letter) in zip(self.stepped_configs(), ' ' + message):
    #         print(configstring(cfg, letter))
    #     print(' ')

    def print_operation(self, message):
        for (cfg, letter) in zip(self.stepped_configs(), ' ' + message):
            print(cfg.config_string(letter))
        #print(' ')

    def print_operation_internal(self, message):
        for (cfg, letter) in zip(self.stepped_configs(), ' ' + message):
            print(cfg.config_string_internal(letter))
            print(' ')

# TBD - Clean up testing script <<<
# TBD - Check spacing of lines, esp at end <<<
# TBD - Testing for enigma encoding list <<<
# ASK - Idiom for printing loops
# ASK - Reversing arguments (like swap)
# ASK - Passing a method as an argument
# ASK - Actual unicode sting length as displayed <<<
# TBD - Fix passing of marking as arugment (needs to percolate up in api hierarchy)
# TBD - Test [x] markup (and others)

