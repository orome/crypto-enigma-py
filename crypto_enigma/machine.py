#!/usr/bin/env python
# encoding: utf8

# Copyright (C) 2015 by Roy Levien.
# This file is part of crypto-enigma, an Enigma Machine simulator.
# released under the BSD-3 License (see LICENSE.txt).

""" 
The main Enigma machine module to import.
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
    """
    An Enigma machine configuration.

    An class representing the state of an Enigma machine, providing functionality for

    * :ref:`generating a machine configuration <config_creation>` from a conventional specification,
    * :ref:`examining the state <config_state>` of a configuration,
    * simulating the :ref:`operation <config_operation>` of a machine by stepping between states, and
    * :ref:`encoding messages <config_encoding>`.

    """

    # TBD - Make private somehow? <<<
    def __init__(self, components, positions, rings):
        """The low level specification of an Enigma configuration.

        The conventional historical specification of an Enigma machine (as used in `~EnigmaConfig.config_enigma`)
        includes redundant elements, and conceals properties that are directly relevant to the operation
        of the machine and the encoding it performs — notably the actual rotational positions of the components.

        A complete "low level" formal characterization of the state of an Enigma machine consists of
        three elements: lists of `~EnigmaConfig.components`, their `~EnigmaConfig.positions`,
        and the settings of their `~EnigmaConfig.rings`.
        Here these lists are in *processing order* — as opposed to the physical order used in conventional
        specifications — and the have positions and ring settings generalized and "padded" for consistency to
        include the plugboard and reflector.

        Note that though it is not likely to be useful, these elements can be used to instantiate an `EnigmaConfig`:

        >>> cfg_conv = EnigmaConfig.config_enigma("B-I-II-III", "ABC", "XO.YM.QL", "01.02.03")
        >>> cfg_intl = EnigmaConfig(cfg_conv.components, cfg_conv.positions, cfg_conv.rings)
        >>> cfg_conv == cfg_intl
        True

        They may also be useful in extending the functionality provided here, for example in constructing
        additional representations of configurations beyond those provided in `config_string`:

        >>> [b'{} {}'.format(c, p) for c, p in zip(cfg_intl.components, cfg_intl.positions)[1:]]
        ['III 1', 'II 1', 'I 1', 'B 1']

        """
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
        """Create an `EnigmaConfig` from strings specifying its state.

        A (safe public, "smart") constructor that does validation and takes a conventional specification as input,
        in the form of four strings.

        Following convention, the elements of these specifications are in physical machine order as the operator
        sees them, which is the reverse of the order in which they are encountered in processing.

        Validation is permissive, allowing for ahistorical collections and numbers of rotors (including reflectors
        at the rotor stage, and trivial degenerate machines; e.g., `config_enigma("-", "A", "", "01")`,
        and any number of (non-contradictory) plugboard wirings (including none).

        Args:
            rotor_names (unicode): The |Walzenlage|_:
                The conventional letter or Roman numeral designations (its `~.components.Component.name`)
                of the rotors, including reflector, separated by dashes (e.g. `'b-β-V-I-II'`).
                (See `components`.)
            window_letters (unicode): The |Walzenstellung|_ (or, incorrectly, the *Grundstellung*):
                The letters visible at the windows (e.g. `'MQR'`).
                (See `windows`.)
            plugs (unicode): The |Steckerverbindungen|_:
                The plugboard specification (its `~.components.Component.name`) as a conventional string of letter
                pairs separated by periods, (e.g., `'AU.ZM.ZL.RQ'`).
                (See `components`.)
            rings (unicode): The |Ringstellung|_:
                The location of the letter ring on each rotor (specifcially, the number on the
                rotor under ring letter **A**), separated by periods (e.g. `'22.11.16'`).
                (See `rings`.)

        Returns:
            EnigmaConfig: A new Enigma machine configuration created from the specification arguments.

        Raises:
            EnigmaValueError: Raised when arguments do not pass validation.

        Example:

            .. _testsetup_properties:

            >>> cfg = EnigmaConfig.config_enigma("c-β-V-III-II", "LQVI", "AM.EU.ZL", "16.01.21.11") # doctest: +SKIP

            .. testsetup:: properties

                cfg = EnigmaConfig.config_enigma("c-β-V-III-II".decode(), u"LQVI", u"AM.EU.ZL", u"16.01.21.11")

        """
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
        """Create an `EnigmaConfig` from a single string specifying its state.

        Args:
            string (unicode): The elements of a conventional specification (as supplied to `config_enigma`)
                joined by spaces into a single string.

        Returns:
            EnigmaConfig: A new Enigma machine configuration created from the specification argument.

        Raises:
            EnigmaValueError: Raised when argument does not pass validation.

        Example:
            This is just a shortcut for invoking `config_enigma` using a sigle string:

            >>> cfg_str = "c-β-V-III-II LQVI AM.EU.ZL 16.01.21.11" # doctest: +SKIP
            >>> EnigmaConfig.config_enigma_from_string(cfg_str) == EnigmaConfig.config_enigma(*cfg_str.split(' ')) # doctest: +SKIP
            True

            Note that the `string` argument corresponds to the string representation of an `EnigmaConfig`

            >>> print(EnigmaConfig.config_enigma_from_string(cfg_str))  # doctest: +SKIP
            c-β-V-III-II LQVI AM.EU.ZL 16.01.21.11

            so that this method is useful for instantiation of an `EnigmaConfig` from such strings (e.g., in files):

            >>> unicode(EnigmaConfig.config_enigma_from_string(cfg_str)) == unicode(cfg_str) # doctest: +SKIP
            True

        """
        split_string = filter(lambda s: s != '', string.split(' '))
        if len(split_string) != 4:
            raise EnigmaValueError('Bad string - {0} should have 4 elements'.format(split_string))

        rotor_names, window_letters, plugs, rings = split_string

        return EnigmaConfig.config_enigma(rotor_names, window_letters, plugs, rings)

    def _window_letter(self, st):
        return chr_A0((self._positions[st] + self._rings[st] - 2) % 26)

    @property
    def components(self):
        """The identities of the components in the Enigma machine.

        For rotors (including the reflector) these correspond to the
        the `~EnigmaConfig.config_enigma.rotor_names` supplied to `config_enigma`, while for the
        plugboard this is just the `~EnigmaConfig.config_enigma.plugs` argument.

        Returns:
            tuple: The `~.components.Component.name` of each `~.components.Component` in an `EnigmaConfig`,
            in processing order.

        Example:
            Using `cfg` as defined :ref:`above <testsetup_properties>`:

            .. doctest:: properties

                >>> cfg.components # doctest: +SKIP
                (u'AM.EU.ZL', u'II', u'III', u'V', u'\u03b2', u'c')

        """
        return self._components

    @property
    def positions(self):
        """The rotational positions of the components in the Enigma machine.

        For rotors, this is to the number on the rotor (not letter ring) that is at the "window position",
        and is computed from the `~EnigmaConfig.config_enigma.window_letters` and
        `~EnigmaConfig.config_enigma.rings` parameters for `config_enigma`.

        This (alone) determines permutations applied to components' `~.components.Component.wiring` to
        produce the :ref:`mapping <config_encoding_mappings>` for a configuration and thus
        the :ref:`message encoding <config_encoding_message>` it performs.

        Note that this is the only property of an enigma machine that changes when it is stepped (see `step`),
        and the changes in the letters visible at the `windows` are the (only) visible manifestation
        of this change.

        Returns:
            tuple: The generalized rotational position of each of the components in an `EnigmaConfig`,
            in machine processing order.

        Example:
            Using `cfg` as defined :ref:`above <testsetup_properties>`:

            .. doctest:: properties

                >>> cfg.positions
                (1, 25, 2, 17, 23, 1)

        Note that for the plugboard and reflector, the position will always be **1** since the former
        cannot rotate, and the latter does not (neither will be different in a new configuration
        generated by `step`)::

            cfg.positions[0] == 1
            cfg.positions[-1] == 1

        """
        return self._positions

    @property
    def rings(self):
        """The ring settings in the Enigma machine.

        For rotors, these are the `~EnigmaConfig.config_enigma.rings` parameter for `config_enigma`.

        Returns:
            tuple: The generalized location of ring letter **A** on the rotor for each of the `components`
            in an `EnigmaConfig`, in machine processing order.

        Example:
            Using `cfg` as defined :ref:`above <testsetup_properties>`:

            .. doctest:: properties

                >>> cfg.rings
                (1, 11, 21, 1, 16, 1)

        Note that for the plugboard and reflector, this will always be **1** since the former lacks a ring,
        and for latter ring position is irrelevant (the letter ring is not visible, and has no effect on when
        turnovers occur)::

            cfg.rings[0] == 1
            cfg.rings[-1] == 1

        """
        return self._rings

    def windows(self):
        """The letters at the windows of an Enigma machine.

        This is the (only) visible manifestation of configuration changes during :ref:`operation <config_operation>`.

        Returns:
            unicode: The letters at the windows in an `EnigmaConfig`, in physical, conventional order.

        Example:
            Using `cfg` as defined :ref:`above <testsetup_properties>`:

            .. doctest:: properties

                >>> cfg.windows()
                u'LQVI'

        """
        # return ''.join(list(reversed([self._window_letter(st) for st in self._stages][1:-1])))
        return ''.join([self._window_letter(st) for st in self._stages][1:-1][::-1])
        # return ''.join([self._window_letter(st) for st in self._stages][-2:0:-1])

    def step(self):
        """Step the Enigma machine to a new machine configuration.

        Step the Enigma machine by rotating the rightmost (first) rotor one position, and other rotors as
        determined by the `positions` of rotors in the machine,
        based on the positions of their `.components.Component.turnovers`.
        In the physical machine, a step occurs in response to each operator keypress,
        prior to processing that key's letter (see `enigma_encoding`).

        Stepping leaves the `components` and `rings` of a configuration unchanged, changing only
        `positions`, which is manifest in changes of the letters visible at the `windows`:

        Returns:
            EnigmaConfig: A new Enigma configuration.

        Examples:
            Using the initial configuration

            >>> cfg = EnigmaConfig.config_enigma("c-γ-V-I-II", "LXZO", "UX.MO.KZ.AY.EF.PL", "03.17.04.01") # doctest: +SKIP

            .. testsetup:: step

                cfg = EnigmaConfig.config_enigma("c-γ-V-I-II".decode(), u"LXZO", u"UX.MO.KZ.AY.EF.PL", u"03.17.04.01")

            the consequences of the stepping process can be observed by examining the `windows` of each
            stepped configuration:

            .. doctest:: step

                >>> print(cfg.windows())
                LXZO
                >>> print(cfg.step().windows())
                LXZP
                >>> print(cfg.step().step().windows())
                LXZQ
                >>> print(cfg.step().step().step().windows())
                LXZR
                >>> print(cfg.step().step().step().step().windows())
                LXZS
                >>> print(cfg.step().step().step().step().step().windows())
                LXZT

            This, and the fact that only positions (and thus window letters) change as the result of stepping,
            can be visualized in more detail using `print_operation`:

            .. doctest:: step

                >>> cfg.print_operation(steps=5, format='config')
                c-γ-V-I-II LXZO UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZP UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZQ UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZR UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZS UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZT UX.MO.KZ.AY.EF.PL 03.17.04.01

        """
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
        """Generate a series of stepped Enigma machine configurations.

        Args:
            steps (int, optional): An optional limit on the number of steps to take in generating configurations.

        Yields:
            EnigmaConfig: The `EnigmaConfig` resulting from applying `step` to the previous one.

        Examples:
            This allows the examples above to be rewritten as

            .. doctest:: step

                >>> for c in cfg.stepped_configs(5):
                ...     print(c.windows())
                LXZO
                LXZP
                LXZQ
                LXZR
                LXZS
                LXZT

                >>> for c in cfg.stepped_configs(5):
                ...     print(c)
                c-γ-V-I-II LXZO UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZP UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZQ UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZR UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZS UX.MO.KZ.AY.EF.PL 03.17.04.01
                c-γ-V-I-II LXZT UX.MO.KZ.AY.EF.PL 03.17.04.01

        """
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
        """The list of |mappings| for each stage of an Enigma machine:

        the encoding performed by the Component at that point in the progress through the machine.

        These are arranged in processing order, beginning with the encoding performed by the plugboard,
        followed by the forward encoding performed by each rotor (see componentMapping),
        then the reflector, followed by the reverse encodings by each rotor, and finally by the plugboard again.

        Returns:
            list of unicode: A list of strings, corresponding the the |mappings| preformed by the corresponding stage
                of the `EnigmaConfig` (see `~.components.Component.mapping`).

        Examples:
            This can be used to obtain lists of mappings for analysis:

            .. testsetup:: config_mappings

                cfg = EnigmaConfig.config_enigma("b-γ-VII-V-IV".decode(), u"VBOA", u"NZ.AY.FG.UX.MO.PL", u"05.16.11.21")

            .. doctest:: config_mappings

                >>> cfg = EnigmaConfig.config_enigma("b-γ-VII-V-IV", "VBOA", "NZ.AY.FG.UX.MO.PL", "05.16.11.21") # doctest: +SKIP
                >>> cfg.stage_mapping_list() # doctest: +ELLIPSIS
                [u'YBCDEGFHIJKPOZMLQRSTXVWUAN', u'DUSKOCLBRFHZNAEXWGQVYMIPJT', ...]

            or more clearly

            .. doctest:: config_mappings

                >>> for m in cfg.stage_mapping_list():
                ...     print(m)
                YBCDEGFHIJKPOZMLQRSTXVWUAN
                DUSKOCLBRFHZNAEXWGQVYMIPJT
                CEPUQLOZJDHTWSIFMKBAYGRVXN
                PCITOWJZDSYERHBNXVUFQLAMGK
                UZYIGEPSMOBXTJWDNAQVKCRHLF
                ENKQAUYWJICOPBLMDXZVFTHRGS
                RKVPFZEXDNUYIQJGSWHMATOLCB
                WOBILTYNCGZVXPEAUMJDSRFQKH
                TSAJBPVKOIRFQZGCEWNLDXMYUH
                NHFAOJRKWYDGVMEXSICZBTQPUL
                YBCDEGFHIJKPOZMLQRSTXVWUAN

            This list is a core part of the "internal" view of machine stage prduced by `config_string`
            (compare the second through the next-to-last lines with the above):

            .. doctest:: config_mappings

                >>> print(cfg.config_string(format='internal'))
                    ABCDEFGHIJKLMNOPQRSTUVWXYZ
                  P YBCDEGFHIJKPOZMLQRSTXVWUAN         NZ.AY.FG.UX.MO.PL
                  1 DUSKOCLBRFHZNAEXWGQVYMIPJT  A  07  IV
                  2 CEPUQLOZJDHTWSIFMKBAYGRVXN  O  05  V
                  3 PCITOWJZDSYERHBNXVUFQLAMGK  B  13  VII
                  4 UZYIGEPSMOBXTJWDNAQVKCRHLF  V  18  γ
                  R ENKQAUYWJICOPBLMDXZVFTHRGS         b
                  4 RKVPFZEXDNUYIQJGSWHMATOLCB         γ
                  3 WOBILTYNCGZVXPEAUMJDSRFQKH         VII
                  2 TSAJBPVKOIRFQZGCEWNLDXMYUH         V
                  1 NHFAOJRKWYDGVMEXSICZBTQPUL         IV
                  P YBCDEGFHIJKPOZMLQRSTXVWUAN         NZ.AY.FG.UX.MO.PL
                    XZJVGSEMTCYUHWQROPFILDNAKB

            Note that, because plugboard mapping is established by paired exchanges of letters
            it is always the case that:

            .. doctest:: config_mappings

                >>> cfg.stage_mapping_list()[0] == cfg.stage_mapping_list()[-1]
                True

            .. todo::
                Add example of how in degenerate case first n are just the wiring (and explain stage as
                reverse too).

        """
        return ([component(comp).mapping(pos, FWD) for (comp, pos) in
                 zip(self._components, self._positions)] +
                [component(comp).mapping(pos, REV) for (comp, pos) in
                 zip(self._components, self._positions)][:-1][::-1])

    # REV - Caching here isn't really needed
    @cached({})
    def enigma_mapping_list(self):
        return list(accumulate(self.stage_mapping_list(), lambda s, m: Mapping(m.encode_string(s))))

    def enigma_mapping(self):
        return self.enigma_mapping_list()[-1]

    @require_unicode('message')
    def enigma_encoding(self, message):
        """Encode a message using the machine configuration.

        Encode a string, interpreted as a message (see `make_message`), using the
        (starting) machine configuration, by stepping (see `step`) the configuration prior to processing each character
        of the message. This produces a new configuration (with new `positions` only) for encoding each character,
        which serves as the "starting" configuration for subsequent processing of the message.

        Args:
            message (unicode): A message to encode.

        Returns:
            unicode: The machine-encoded message.

        Examples:
            Given machine configuration

            >>> cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LFAP", "UX.MO.KZ.AY.EF.PL", "03.17.04.11") # doctest: +SKIP

            .. testsetup:: enigma_encoding

                cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II".decode("UTF-8"), u"LFAP", u"UX.MO.KZ.AY.EF.PL", u"03.17.04.11")

            the message `'KRIEG'` is encoded to `'GOWNW'`:

            .. doctest:: enigma_encoding

                >>> cfg.enigma_encoding('KRIEG')
                u'GOWNW'

            The details of this encoding and its relationship to stepping from one configuration to another are illustrated
            using `print_operation`:

            .. doctest:: enigma_encoding

                >>> cfg.print_operation("KRIEG", format='windows', show_encoding=True, show_step=True)
                0000  LFAP
                0001  LFAQ  K > G
                0002  LFAR  R > O
                0003  LFAS  I > W
                0004  LFAT  E > N
                0005  LFAU  G > W

            Note that because of the way the Enigma machine is designed, it is always the case
            (provided that `msg` is all uppercase letters) that::

                cfg.enigma_encoding(cfg.enigma_encoding(msg)) == msg

        """
        message = EnigmaConfig.make_message(message)

        return ''.join([step_config.enigma_mapping().encode_char(letter) for
                        (letter, step_config) in zip(message, self.step().stepped_configs())])

    # ASK - Equvalent to Haskell read (if this is like show, or is _repr_ show; eval(repr(obj)) )? <<<
    def __unicode__(self):
        return "{0} {1} {2} {3}".format('-'.join(self._components[1:][::-1]),
                                        self.windows(),
                                        self._components[0],
                                        '.'.join(['{:02d}'.format(r) for r in self._rings[1:-1]][::-1]))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return '{0} ({1})'.format(object.__repr__(self), unicode(self)).encode('utf-8')

    def __eq__(self, cfg):
        return all([self.components == cfg.components, self.positions == cfg.positions,  self.rings == cfg.rings])

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
        return string.index(mapping.encode_char(letter)) if letter in string else -1

    # Ensures a single uppercase character ("those that are valid Enigma input") or space, defaulting to a space
    @staticmethod
    def _make_enigma_char(letter):
        return filter(lambda l: l in LETTERS + ' ', (letter + ' ').upper())[0]

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
                            zip([Mapping(LETTERS)] + cfg_mapping_list + [cfg_mapping],
                                [letter] * (len(self._stages) * 2 + 1),
                                [Mapping(LETTERS)] + stg_mapping_list + [cfg_mapping])]

        stg_labels = reflect_info(['P'] + list(self._stages)[1:-1] + ['R'])
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
                "{0} {1}".format(self.enigma_mapping().encode_char(letter) + ' <' if letter in LETTERS else '   ',
                                 EnigmaConfig._marked_mapping(cfg_mapping, letter_locations[-1], mark_func))
                )

    @staticmethod
    @require_unicode('string')
    def make_message(string):
        """Convert a string to valid Enigma machine input.

        Replace any symbols for which there are standard Kriegsmarine substitutions,
        remove any remaining non-letter characters, and convert to uppercase.
        This function is applied automatically to `message` arguments for functions defined here
        (`enigma_encoding`).

        Args:
            string (unicode): A string to convert to valid Enigma machine input.

        Returns:
            unicode: A string of valid Enigma machine input characters.

        """
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
                encoding_string = '  {0} > {1}'.format(letter, self.enigma_mapping().encode_char(letter))

            if format in EnigmaConfig._FMTS_INTERNAL:
                return self._config_string_internal(letter, mark_func)
            elif format in EnigmaConfig._FMTS_SINGLE:
                return self._config_string(letter, mark_func)
            elif format in EnigmaConfig._FMTS_WINDOWS:
                return self.windows() + encoding_string
            elif format in EnigmaConfig._FMTS_CONFIG:
                return str(self) + encoding_string
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

    @require_unicode('message')
    def print_operation_internal(self, message, mark_func=None):
        """
        .. deprecated:: 0.0.2
            This function has been removed; use :func:`print_operation` instead.
        """
        self.print_operation(message, format='internal', mark_func=mark_func)

    @staticmethod
    @require_unicode('msg')
    def _postprocess(msg):
        return '\n'.join(chunk_of(' '.join(chunk_of(msg, 4)), 60))

    @require_unicode('message')
    def print_encoding(self, message):
        print(EnigmaConfig._postprocess(self.enigma_encoding(EnigmaConfig.make_message(message))))


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
