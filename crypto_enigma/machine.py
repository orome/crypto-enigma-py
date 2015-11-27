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

# REV - Additional performance improvements
# A large speed improvement comes from caching the encodings of rotors when first computed for a given position.
# This is effective because upper rotors don't change frequently so such cached mappings are reused many times. And
# because even the lower rotors will assume a maximum of 26 distinct positions, the cache will always be small.
# Improvements from implementing mappings as lists of numbers rather than strings are negligible and not worth the loss
# of clarity.
# The mark_func argument should take a single character and return a string representing that character, "marked" to
# highlight it in a the string representing a mapping. Ideally, the number of added printed characters should be even.
from __future__ import (absolute_import, print_function, division, unicode_literals)

from unicodedata import combining

from .components import *


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

        # TBD - Assertions plugboard <<<
        assert all(name in rotors for name in components[1:-1])
        assert components[-1] in reflectors
        assert len(rings) == len(positions) == len(components)
        assert all(1 <= rng <= 26 for rng in rings)
        assert all(1 <= pos <= 26 for pos in positions)
        #assert all(chr_A0(pos) in LETTERS for pos in positions)

        self._components = tuple(components)
        self._positions = tuple(positions)
        self._rings = tuple(rings)
        self._stages = tuple(range(0, len(self._components)))

    @staticmethod
    @require_unicode('rotor_names', 'window_letters', 'plugs', 'rings')
    def config_enigma(rotor_names, window_letters, plugs, rings):

        rotor_names_list = rotor_names.split('-')
        ring_numbers = [int(x) for x in rings.split('.')]

        # TBD - Validation for plugboard <<<
        # A bunch of checks to provide better feedback than (and befor lower-level) assertions
        for name in rotor_names_list[1:]:
            if name not in rotors:
                raise EnigmaValueError('Bad configuration - Invalid rotor name, {0}'.format(name))
        if rotor_names_list[0] not in reflectors:
            raise EnigmaValueError('Bad configuration: invalid reflector name, {0}'.format(rotor_names_list[0]))
        if not (len(ring_numbers) == len(window_letters) == len(rotor_names_list)-1):
            raise EnigmaValueError('Bad configuration: number rotors ({0}), rings ({1}), and window letters ({2}) must match'.format(
                len(rotor_names_list)-1, len(ring_numbers), len(window_letters)
            ))
        for rng in ring_numbers:
            if not (1 <= rng <= 26):
                raise EnigmaValueError('Bad configuration: invalid ring position number, {0}'.format(rng))
        for wind in window_letters:
            if wind not in LETTERS:
                raise EnigmaValueError('Bad configuration: window letter, {0}'.format(wind))

        comps = (rotor_names + '-' + plugs).split('-')[::-1]
        winds = [num_A0(c) for c in 'A' + window_letters + 'A'][::-1]
        rngs = [int(x) for x in ('01.' + rings + '.01').split('.')][::-1]

        return EnigmaConfig(comps, [((w - r + 1) % 26) + 1 for w, r in zip(winds, rngs)], rngs)

    @staticmethod
    @require_unicode('string')
    def config_enigma_from_string(string):

        split_string = filter(lambda s: s != '', string.split(' '))
        if len(split_string) != 4:
            raise EnigmaValueError('Bad string - {0} should have 4 elements'.format(split_string))

        rotor_names, window_letters, plugs, rings = split_string

        return EnigmaConfig.config_enigma(rotor_names, window_letters, plugs, rings)

    def _window_letter(self, st):
        return chr_A0((self._positions[st] + self._rings[st] - 2) % 26)

    def windows(self):
        # return ''.join(list(reversed([self._window_letter(st) for st in self._stages][1:-1])))
        return ''.join([self._window_letter(st) for st in self._stages][1:-1][::-1])
        # return ''.join([self._window_letter(st) for st in self._stages][-2:0:-1])

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

    # REV - Caching here isn't really needed
    @cached({})
    def stage_mapping_list(self):
        return ([component(comp).mapping(pos, FWD) for (comp, pos) in
                 zip(self._components, self._positions)] +
                [component(comp).mapping(pos, REV) for (comp, pos) in
                 zip(self._components, self._positions)][:-1][::-1])

    # REV - Caching here isn't really needed
    @cached({})
    def enigma_mapping_list(self):
        return list(accumulate(self.stage_mapping_list(), lambda s, m: encode_string(m, s)))

    def enigma_mapping(self):
        # return reduce(lambda string, mapping: encode_string(mapping, string), self.stage_mapping_list(), LETTERS)
        return self.enigma_mapping_list()[-1]

    @require_unicode('message')
    def enigma_encoding(self, message):

        message = EnigmaConfig.make_message(message)

        return ''.join([encode_char(step_config.enigma_mapping(), letter) for
                        (letter, step_config) in zip(message, self.step().stepped_configs())])

    # ASK - Equvalent to Haskell read (if this is like show, or is _repr_ show; eval(repr(obj)) )? <<<
    def __unicode__(self):
        return "{0} {1} {2} {3}".format('-'.join(self._components[1:][::-1]),
                                        self.windows(),
                                        self._components[0],
                                        '.'.join(['{:02d}'.format(r) for r in self._rings[1:-1]][::-1]))

    def __str__(self):
        return unicode(self).encode('utf-8')

    # __repr__ = __str__
    def __repr__(self):
        # return '<{0}.{1} object at {2}> ({3})'.format(self.__module__, type(self).__name__, hex(id(self)),str(self))
        return '{0} ({1})'.format(object.__repr__(self), unicode(self))

    @staticmethod
    def _marked_mapping(mapping, i, mark_func=None):

        def marked_char(c):
            if mark_func is None:
                # REV - Why does this end up here if mark_func is supplied with non-Unicode?
                return c + '\u0332\u0305'
                #return '[' + c + ']'
                # REV - Would be nice, but has limited support: http://www.fileformat.info/info/unicode/char/20de/
                # return c + u'\u20DE'
            else:
                return mark_func(c)

        pads = ' ' * ((sum(not combining(c) for c in marked_char('A')) - 1) // 2)

        return mapping[:i] + marked_char(mapping[i]) + mapping[i + 1:] if 0 <= i < len(mapping) else pads + mapping + pads

    # TBD - Add assertions to all that they get Unicode <<<
    @staticmethod
    def _locate_letter(mapping, letter, string):

        # locate the index of the encoding with mapping of letter, in string
        # REV - Use of out of bounds index (-1) as failure return value; callers must check bounds (see above) <<<
        return string.index(encode_char(mapping, letter)) if letter in string else -1

    # Ensures a single uppercase character ("those that are valid Enigma input") or space, defaulting to a space
    @staticmethod
    def _make_enigma_char(letter):
        return filter(lambda l: l in LETTERS + ' ', (letter + ' ').upper())[0]

    # @staticmethod
    # def _make_valid_message(string):
    #     return ''.join([EnigmaConfig._make_valid_letter(l) for l in EnigmaConfig.preprocess(string)])

    # @staticmethod
    # def _is_valid_letter(letter):
    #     return len(letter) == 1 and letter in LETTERS + ' '
    #
    # @staticmethod
    # def _is_valid_string(string):
    #     return all(EnigmaConfig._is_valid_letter(l) for l in string)

    def _config_string(self, letter, mark_func=None):

        cfg_mapping = self.enigma_mapping()

        return '{0} {1}  {2}  {3}'.format(letter + ' >' if letter in LETTERS else '   ',
                                          EnigmaConfig._marked_mapping(cfg_mapping,
                                                                       EnigmaConfig._locate_letter(cfg_mapping,
                                                                                                   letter,
                                                                                                   cfg_mapping),
                                                                       mark_func),
                                          self.windows(),
                                          ' '.join(['{:02d}'.format(p) for p in self.positions[1:-1]][::-1]))

    def _config_string_internal(self, letter, mark_func=None):

        cfg_mapping = self.enigma_mapping()
        cfg_mapping_list = self.enigma_mapping_list()
        stg_mapping_list = self.stage_mapping_list()

        def reflect_info(stg_info): return stg_info + stg_info[::-1][1:]

        def pad_info(stg_info, pad): return [pad] + stg_info + ([pad] * len(self.positions))

        # REV - Better way that avoids recalcs of cfg_mapping and cfg_mapping_list?
        letter_locations = [EnigmaConfig._locate_letter(m, l, s) for (m, l, s) in
                            zip([LETTERS] + cfg_mapping_list + [cfg_mapping],
                                [letter] * (len(self.stages) * 2 + 1),
                                [LETTERS] + stg_mapping_list + [cfg_mapping])]

        stg_labels = reflect_info(['P'] + list(self.stages)[1:-1] + ['R'])
        stg_mappings = [EnigmaConfig._marked_mapping(m, i, mark_func) for (m, i) in zip(stg_mapping_list,
                                                                                        letter_locations[1:-1])]
        stg_windows = pad_info(list(self.windows())[::-1], ' ')
        stg_positions = pad_info(['{:02d}'.format(p) for p in self.positions][1:-1], '  ')
        stg_coponents = reflect_info(self.components)

        return ("{0} {1}\n".format(letter + ' >' if letter in LETTERS else '   ',
                                   EnigmaConfig._marked_mapping(LETTERS, letter_locations[1], mark_func)) +
                ''.join(['  {0} {1}  {2}  {3}  {4}\n'.format(stg_lbl, stg_map, stg_wind, stg_pos, stg_comp)
                         for (stg_lbl, stg_map, stg_wind, stg_pos, stg_comp) in zip(stg_labels,
                                                                                    stg_mappings,
                                                                                    stg_windows,
                                                                                    stg_positions,
                                                                                    stg_coponents)]) +
                "{0} {1}".format(encode_char(self.enigma_mapping(), letter) + ' <' if letter in LETTERS else '   ',
                                 EnigmaConfig._marked_mapping(cfg_mapping, letter_locations[-1], mark_func))
                )

    @staticmethod
    @require_unicode('string')
    def make_message(string):

        subs = [(' ', ''), ('.', 'X'), (',', 'Y'), ("'", 'J'), ('>', 'J'), ('<', 'J'), ('!', 'X'),
                ('?', 'UD'), ('-', 'YY'), (':', 'XX'), ('(', 'KK'), (')', 'KK'),
                ('1', 'YQ'), ('2', 'YW'), ('3', 'YE'), ('4', 'YR'), ('5', 'YT'),
                ('6', 'YZ'), ('7', 'YU'), ('8', 'YI'), ('9', 'YO'), ('0', 'YP')]

        msg = filter(lambda c: c in LETTERS, reduce(lambda s, (o, n): s.replace(o, n), subs, string.upper()))
        assert all(letter in LETTERS for letter in msg)

        return msg

    # TBD - Additional formats, e.g., components listed, etc.
    _FMTS_INTERNAL = ['internal', 'detailed', 'schematic']
    _FMTS_SINGLE = ['single', 'summary']
    _FMTS_WINDOWS = ['windows', 'winds']
    _FMTS_CONFIG = ['config', 'configuration', 'spec', 'specification']
    _FMTS_ENCODING = ['encoding']
    _FMTS_DEBUG = ['debug']

    # TBD - Add encoding note to config and windows (e.g with P > K) <<<
    # TBD - Add components format that lists the components and their attributes <<<
    @require_unicode('letter')
    def config_string(self, letter='', format='single', show_encoding=False, mark_func=None):

            # TBD - Check that mark_func returns Unicode, or that it 'succeeds'? - #13
            letter = EnigmaConfig._make_enigma_char(letter)

            encoding_string = ''
            if letter in LETTERS and (show_encoding or format in EnigmaConfig._FMTS_ENCODING):
                encoding_string = '  {0} > {1}'.format(letter, encode_char(self.enigma_mapping(),letter))

            if format in EnigmaConfig._FMTS_INTERNAL:
                return self._config_string_internal(letter, mark_func)
            elif format in EnigmaConfig._FMTS_SINGLE:
                return self._config_string(letter, mark_func)
            elif format in EnigmaConfig._FMTS_WINDOWS:
                return self.windows() + encoding_string
            elif format in EnigmaConfig._FMTS_CONFIG:
                return unicode(self) + encoding_string
            elif format in EnigmaConfig._FMTS_DEBUG:
                return self.__repr__() + encoding_string
            elif format in EnigmaConfig._FMTS_ENCODING:
                return encoding_string[2:]
            else:
                raise EnigmaDisplayError('Bad argument - Unrecognized format, {0}'.format(format))

    @require_unicode('letter')
    def config_string_internal(self, letter='', mark_func=None):
        """
        .. deprecated:: 0.0.2
            This function has been removed; use :func:`config_string` instead.
        """
        return self.config_string(letter, format='internal', mark_func=mark_func)

    @require_unicode('message')
    def print_operation(self, message='', steps=None, overwrite=False, format='single', initial=True, delay=0.1,
                        show_step=False, show_encoding=False, mark_func=None):

        def print_config_string(cfg_str):
            if step_num != 0 or initial:
                if show_step:
                    if format=='internal':
                        cfg_str = '{0:04d}\n{1}'.format(step_num, cfg_str)
                    else:
                        cfg_str = '{0:04d}  {1}'.format(step_num, cfg_str)
                if overwrite and step_num <= steps:
                    print_over(cfg_str, (0 if initial else 1) < step_num, delay)
                else:
                    print(cfg_str)
                if not overwrite and format=='internal' and step_num < steps:
                    print('')

        message = EnigmaConfig.make_message(message)
        if message != '':
            steps = len(message) if steps is None else min(steps, len(message))
        elif steps is not None:
            message = ' ' * steps
        else:
            message = ' '
            steps = 1

        for (step_num, cfg, letter) in zip(range(0, steps+1), self.stepped_configs(), ' ' + message[:steps]):
            if not initial and step_num == 0:
                continue
            print_config_string(cfg.config_string(letter, format=format, show_encoding=show_encoding, mark_func=mark_func))

    # def print_operation(self, message, mark_func=None):
    #     for (cfg, letter) in zip(self.stepped_configs(), ' ' + EnigmaConfig.preprocess(message)):
    #         print(cfg.config_string(letter, mark_func))
    #         # print(' ')

    @require_unicode('message')
    def print_operation_internal(self, message, mark_func=None):
        """
        .. deprecated:: 0.0.2
            This function has been removed; use :func:`print_operation` instead.
        """
        self.print_operation(message, format='internal', mark_func=mark_func)
        # for (cfg, letter) in zip(self.stepped_configs(), ' ' + EnigmaConfig.preprocess(message)):
        #     print(cfg.config_string_internal(letter, mark_func))
        #     print(' ')

    @staticmethod
    @require_unicode('msg')
    def postprocess(msg):
        return '\n'.join(chunk_of(' '.join(chunk_of(msg, 4)), 60))

    @require_unicode('message')
    def print_encoding(self, message):
        print(EnigmaConfig.postprocess(self.enigma_encoding(EnigmaConfig.make_message(message))))


class EnigmaError(Exception):
    pass


class EnigmaValueError(EnigmaError, ValueError):
    pass


class EnigmaDisplayError(EnigmaError):
    pass

# TBD - Tidy printing code so that the structures and names in config_string_internal and config_string match <<<
# TBD - Check spacing of lines, esp at end in .._string and print_... methods <<<
# ASK - Idiom for printing loops?
# REV - Keep list(reverse( conversions as [::-1] throughout?
# TBD - Break out heavy validation stuff into another layer to keep core functionality separate?
# REV - Use of EnigmaError vs. assert (be systematic about distinction) <<<