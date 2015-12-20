#!/usr/bin/env python
# encoding: utf8

# Copyright (C) 2015 by Roy Levien.
# This file is part of crypto-enigma, an Enigma Machine simulator.
# released under the BSD-3 License (see LICENSE.txt).

""" 
This module supports all of the functionality of an Enigma machine using an `EnigmaConfig` class and
several utility functions, which support examination of its state
(including the details of the cyphers used for encoding messages), stepping during operation, and encoding messages.

.. todo::
    Flesh out and link to sections.

.. todo::
    Fix and document import organization.
"""


# The mark_func argument should take a single character and return a string representing that character, "marked" to
# highlight it in a the string representing a mapping. Ideally, the number of added printed characters should be even.
from __future__ import (absolute_import, print_function, division, unicode_literals)

from unicodedata import combining

from .components import *
from .exceptions import *


class EnigmaConfig(object):
    """An Enigma machine configuration.

    A class representing the state of an Enigma machine, providing functionality for

    * :ref:`generating a machine configuration <config_creation>` from a conventional specification,
    * :ref:`examining the state <config_state>` of a configuration,
    * simulating the :ref:`operation <config_operation>` of a machine by stepping between states, and
    * :ref:`encoding messages <config_encoding>`.

    """

    def __init__(self, components, positions, rings):
        """The core properties of an `EnigmaConfig` embody a low level specification of an Enigma configuration.

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
        produce the :ref:`mapping <config_state_mappings>` for a configuration and thus
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
        """The list of mappings for each stage of an Enigma machine.

        The list of |mappings| for each stage of in an `EnigmaConfig`:
        The encoding performed by the `~.components.Component` *at that point* in the progress through the machine.

        These are arranged in processing order, beginning with the encoding performed by the plugboard,
        followed by the forward (see `~.component.Direction`) encoding performed by each rotor
        (see `~.components.Component.mapping`), then the reflector, followed by the reverse encodings by each rotor,
        and finally by the plugboard again.

        Returns:
            list of Mapping: A list of |mappings| preformed by the corresponding stage
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
        return ([component(comp).mapping(pos, Direction.FWD) for (comp, pos) in
                 zip(self._components, self._positions)] +
                [component(comp).mapping(pos, Direction.REV) for (comp, pos) in
                 zip(self._components, self._positions)][:-1][::-1])

    # REV - Caching here isn't really needed
    @cached({})
    def enigma_mapping_list(self):
        """The list of progressive mappings of an Enigma machine at each stage.

        The list of |mappings| an `EnigmaConfig` has performed by each stage:
        The encoding performed by the `EnigmaConfig` as a whole *up to that point* in the progress through the machine.

        These are arranged in processing order, beginning with the encoding performed by the plugboard,
        followed by the forward (see `~.component.Direction`) encoding performed up to each rotor
        (see `~.components.Component.mapping`), then the reflector, followed by the reverse encodings up to each
        rotor, and finally by the plugboard again.

        Returns:
            list of Mapping: A list of |mappings| preformed by the `EnigmaConfig` up to the corresponding stage
                of the `EnigmaConfig` (see `~.components.Component.mapping`).

        Examples:
            This can be used to obtain lists of mappings for analysis:

            .. doctest:: config_mappings

                >>> cfg = EnigmaConfig.config_enigma("b-γ-VII-V-IV", "VBOA", "NZ.AY.FG.UX.MO.PL", "05.16.11.21") # doctest: +SKIP
                >>> cfg.enigma_mapping_list() # doctest: +ELLIPSIS
                [u'YBCDEGFHIJKPOZMLQRSTXVWUAN', u'JUSKOLCBRFHXETNZWGQVPMIYDA', ...]

            or more clearly

            .. doctest:: config_mappings

                >>> for m in cfg.enigma_mapping_list():
                ...     print(m)
                YBCDEGFHIJKPOZMLQRSTXVWUAN
                JUSKOLCBRFHXETNZWGQVPMIYDA
                DYBHITPEKLZVQASNROMGFWJXUC
                TGCZDFNOYEKLXPUHVBRJWASMQI
                VPYFIEJWLGBXHDKSCZAORUQTNM
                TMGUJAIHOYNRWQCZKSELXFDVBP
                MIEANRDXJCQWOSVBUHFYLZPTKG
                XCLWPMIQGBUFEJROSNTKVHADZY
                YAFMCQOEVSDPBIWGNZLRXKTJHU
                UNJVFSEOTCAXHWQRMLGIPDZYKB
                XZJVGSEMTCYUHWQROPFILDNAKB

            Since these may be thought of as cumulative encodings by the machine, the final element of the list
            will be the mapping used by the machine for encoding:

            .. doctest:: config_mappings

                >>> cfg.enigma_mapping() == cfg.enigma_mapping_list()[-1]
                True

        """
        return list(accumulate(self.stage_mapping_list(), lambda s, m: Mapping(m.encode_string(s))))

    def enigma_mapping(self):
        """The mapping used by an Enigma machine for encoding.

        The |mapping| used by an `EnigmaConfig` to encode a letter entered at the keyboard.

        Returns:
            Mapping: The |mapping| used by the `EnigmaConfig` encode a single character.

        Examples:
            This is the final element in the corresponding `enigma_mapping_list`:

            .. doctest:: config_mappings

                >>> cfg.enigma_mapping()
                u'XZJVGSEMTCYUHWQROPFILDNAKB'

        """
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

        Replace any symbols for which there are standard *Kriegsmarine* substitutions,
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
        """A string representing a schematic of an Enigma machine's state.

        A string representing the stat of an `EnigmaConfig` in a selected format (see examples),
        optionally indicating how specified character is encoded by the configuration.

        Args:
            letter (unicode, optional): A character to indicate the encoding of by the `EnigmaConfig`.
            format (str, optional): A string specifying the format used to display the `EnigmaConfig`.
            show_encoding (bool, optional): Whether to indicate the encoding for formats that do not
                include it by default.
            mark_func (function, optional): A `function` that highlights its argument by taking a single character
                as an argument and returning a string with additional characters added to (usually surrounding)
                that charater. Used in cases where default method of highlighting the encoded-to character
                (see `~.cypher.Mapping`) does not display correctly or clearly.

        Returns:
            str: A string schematically representing an `EnigmaConfig`

        Examples:
            A variety of formats are available for representing the state of the Enigma machine:

            .. testsetup:: enigma_config_string

                cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II".decode("UTF-8"), u"LFAQ", u"UX.MO.KZ.AY.EF.PL", u"03.17.04.11")

            .. doctest:: enigma_config_string

                >>> cfg = EnigmaConfig.config_enigma("b-γ-V-VIII-II", "LFAQ", "UX.MO.KZ.AY.EF.PL",u"03.17.04.11") # doctest: +SKIP
                >>> print(cfg.config_string(format='single'))
                    CMAWFEKLNVGHBIUYTXZQOJDRPS  LFAQ  10 16 24 07
                >>> print(cfg.config_string(format='internal'))
                    ABCDEFGHIJKLMNOPQRSTUVWXYZ
                  P YBCDFEGHIJZPONMLQRSTXVWUAK         UX.MO.KZ.AY.EF.PL
                  1 LORVFBQNGWKATHJSZPIYUDXEMC  Q  07  II
                  2 BJYINTKWOARFEMVSGCUDPHZQLX  A  24  VIII
                  3 ILHXUBZQPNVGKMCRTEJFADOYSW  F  16  V
                  4 YDSKZPTNCHGQOMXAUWJFBRELVI  L  10  γ
                  R ENKQAUYWJICOPBLMDXZVFTHRGS         b
                  4 PUIBWTKJZSDXNHMFLVCGQYROAE         γ
                  3 UFOVRTLCASMBNJWIHPYQEKZDXG         V
                  2 JARTMLQVDBGYNEIUXKPFSOHZCW         VIII
                  1 LFZVXEINSOKAYHBRGCPMUDJWTQ         II
                  P YBCDFEGHIJZPONMLQRSTXVWUAK         UX.MO.KZ.AY.EF.PL
                    CMAWFEKLNVGHBIUYTXZQOJDRPS
                >>> print(cfg.config_string(format='windows'))
                LFAQ
                >>> print(cfg.config_string(format='config'))
                b-γ-V-VIII-II LFAQ UX.MO.KZ.AY.EF.PL 03.17.04.11
                >>> print(cfg.config_string(format='encoding', letter='K'))
                K > G

            Use `format='single'` or omit the argument to display a summary of the Enigma machine configuration
            as its `~.cypher.Mapping` (see `enigma_mapping`), the letters at the `windows`,
            and the `positions` of the rotors. If a valid message character is provided as a value for `letter`,
            that is indicated as input and the letter it is encoded to is highlighted.

            For example,

            .. doctest:: enigma_config_string

                >>> print(cfg.config_string(letter='K'))
                K > CMAWFEKLNVG̲̅HBIUYTXZQOJDRPS  LFAQ  10 16 24 07

            shows the process of encoding of the letter **K** to **G**.

            The default method of highlighting the encoded-to character (see `~.cypher.Mapping`) may not display
            correctly on all systems, so the `marc_func` argument can be used to define a simpler marking that
            does:

            .. doctest:: enigma_config_string

                >>> print(cfg.config_string(letter='K', mark_func=lambda c: '[' + c + ']'))
                K > CMAWFEKLNV[G]HBIUYTXZQOJDRPS  LFAQ  10 16 24 07
                >>> print(cfg.config_string(letter='K', mark_func=lambda c: '(' + c + ')'))
                K > CMAWFEKLNV(G)HBIUYTXZQOJDRPS  LFAQ  10 16 24 07

            Use `format='internal'` to display a summary of the Enigma machine configuration as a detailed
            schematic of each processing stage of the `EnigmaConfig` (proceeding from top to bottom), in which

            * each line indicates the `~.cypher.Mapping` preformed by the component at that stage
              (see `stage_mapping_list`);
            * each line begins with an indication of the stage (rotor number, **P** for plugboard, or **R**
              for reflector) at that stage, and ends with the specification (see `~.components.Component.name`)
              of the component at that stage;
            * rotors additionally indicate their window letter, and position; and
            * if a valid `letter` is provided, it is indicated as input and its
              encoding at each stage is marked;

            The schematic is followed by the mapping for the machine as a whole (as
            for the `'single'` format), and preceded by a (trivial, no-op) keyboard "mapping"
            for reference.

            For example,

            .. doctest:: enigma_config_string

                >>> print(cfg.config_string(letter='K', format='internal', mark_func=lambda c: '(' + c + ')'))
                K > ABCDEFGHIJ(K)LMNOPQRSTUVWXYZ
                  P YBCDFEGHIJ(Z)PONMLQRSTXVWUAK         UX.MO.KZ.AY.EF.PL
                  1 LORVFBQNGWKATHJSZPIYUDXEM(C)  Q  07  II
                  2 BJ(Y)INTKWOARFEMVSGCUDPHZQLX  A  24  VIII
                  3 ILHXUBZQPNVGKMCRTEJFADOY(S)W  F  16  V
                  4 YDSKZPTNCHGQOMXAUW(J)FBRELVI  L  10  γ
                  R ENKQAUYWJ(I)COPBLMDXZVFTHRGS         b
                  4 PUIBWTKJ(Z)SDXNHMFLVCGQYROAE         γ
                  3 UFOVRTLCASMBNJWIHPYQEKZDX(G)         V
                  2 JARTML(Q)VDBGYNEIUXKPFSOHZCW         VIII
                  1 LFZVXEINSOKAYHBR(G)CPMUDJWTQ         II
                  P YBCDFE(G)HIJZPONMLQRSTXVWUAK         UX.MO.KZ.AY.EF.PL
                G < CMAWFEKLNV(G)HBIUYTXZQOJDRPS

            shows the process of encoding of the letter **K** to **G**:

            * **K** is entered at the keyboard, which is then
            * encoded by the plugboard (**P**), which includes **KZ** in its specification (see Name),
              to **Z**, which is then
            * encoded by the first rotor (**1**), a **II** rotor in the 06 position (and **Q** at the window),
              to **C**, which is then
            * encoded by the second rotor (**2**), a **VIII** rotor in the 24 position (and **A** at the window),
              to **Y**, which is then
            * encoded by the third rotor (**3**), a **V** rotor in the 16 position (and **F** at the window),
              to **S**, which is then
            * encoded by the fourth rotor (**4**), a **γ** rotor in the 10 position (and **L** at the window),
              to **J**, which is then
            * encoded by the reflector rotor (**U**), a **b** reflector,
              to **I**, which reverses the signal sending it back through the rotors, where it is then
            * encoded in reverse by the fourth rotor (**4**), to **Z**, which is then
            * encoded in reverse by the third rotor (**3**), to **G**, which is then
            * encoded in reverse by the second rotor (**2**), to **Q**, which is then
            * encoded in reverse by the first rotor (**1**), to **G**, which is then
            * left unchanged by the plugboard (**P**), and finally
            * displayed as **G**.

            Note that (as follows from Mapping) the position of the marked letter at each stage is the alphabetic
            position of the marked letter at the previous stage.

            This can be represented schematically (with input arriving and output exiting on the left) as

            .. image:: _static/figs/configinternal.jpg
                 :scale: 85 %
                 :alt: Detailed schematic of encoding of K to G
                 :align: center

            Use `format='windows'` to simply show the letters at the `windows` as the operator would see them.

            .. doctest:: enigma_config_string

                >>> print(cfg.config_string(format='windows'))
                LFAQ

            And use `format='config'` to simply show a conventional specification of an `EnigmaConfig`
            (as used for `config_enigma_from_string`):

            .. doctest:: enigma_config_string

                >>> print(cfg.config_string(format='config'))
                b-γ-V-VIII-II LFAQ UX.MO.KZ.AY.EF.PL 03.17.04.11

            For both of the preceeding two formats, it is possible to also indicate the encoding of a character
            (not displayed by default) by setting `show_encoding` to `True`:

            .. doctest:: enigma_config_string

                >>> print(cfg.config_string(format='windows', letter='K'))
                LFAQ
                >>> print(cfg.config_string(format='windows', letter='K', show_encoding=True))
                LFAQ  K > G
                >>> print(cfg.config_string(format='config', letter='K'))
                b-γ-V-VIII-II LFAQ UX.MO.KZ.AY.EF.PL 03.17.04.11
                >>> print(cfg.config_string(format='config', letter='K', show_encoding=True))
                b-γ-V-VIII-II LFAQ UX.MO.KZ.AY.EF.PL 03.17.04.11  K > G

            Use `format='encoding'` to show this encoding alone:

            .. doctest:: enigma_config_string

                >>> print(cfg.config_string(format='encoding', letter='K'))
                K > G

            Note that though the examples above have been wrapped in `print` for clarity, these functions
            return strings:

            .. doctest:: enigma_config_string

                >>> cfg.config_string(format='windows', letter='K', show_encoding=True)
                u'LFAQ  K > G'
                >>> cfg.config_string(format='internal').split('\\n') # doctest: +ELLIPSIS
                [u'    ABCDEFGHIJKLMNOPQRSTUVWXYZ', u'  P YBCDFEGHIJZPONMLQRSTXVWUAK         UX.MO.KZ.AY.EF.PL', ...]

        """
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
            This function has been removed; use `config_string` instead.
        """
        return self.config_string(letter, format='internal', mark_func=mark_func)

    @require_unicode('message')
    def print_operation(self, message='', steps=None, overwrite=False, format='single', initial=True, delay=0.1,
                        show_step=False, show_encoding=False, mark_func=None):
        """Show the operation of the Enigma machine as a series of configurations.

        Print out the operation of the Enigma machine as a series of `EnigmaConfig`, as it encodes a `message` and/or
        for a specified number of `steps`.

        Args:
            message (unicode): A message to encode. Characters that are not letters will be replaced with
                standard *Kriegsmarine* substitutions or be removed (see `make_message`).
                Each character will be used as a `letter` in the `config_string` specified by the `format`.
            steps (int, optional): A number of steps to run; if omitted when a `message` is provided,
                will default to the length of the message; otherwise defaults to 1
            overwrite (bool, optional): Whether to overwrite the display of each step after a pause.
                (May result in garbled output on some systems.)
            format (str, optional): A string specifying the format used to display the `EnigmaConfig` at each
                step of message processing; see `config_string`.
            initial (bool, optional): Whether to show the initial starting step; the `EnigmaConfig` before
                encoding begins.
            delay (float, optional): The number of seconds to wait (see `time.sleep`) between the display of
                each processing step; defaults to 0.2.
            show_step (bool, optional): Whether to include the step number in the display.
            show_encoding (bool, optional): Whether to indicate the encoding of each character for formats
                that do not include it by default; see `config_string`.
            mark_func (function, optional): A `function` that highlights its argument by taking a single character
                as an argument and returning a string with additional characters added to (usually surrounding)
                that charater. Used in cases where default method of highlighting the encoded-to character
                (see `~.cypher.Mapping`) does not display correctly or clearly.

        Examples:
            (For details on differences among formats used for displaying each step, see the
            examples for `config_string`.)

            Show the operation of a machine for 10 steps, indicating step numbers:

            .. testsetup:: enigma_print_operation

                cfg = EnigmaConfig.config_enigma("B-I-III-I".decode("UTF-8"),u"EMO", u"UX.MO.AY", u"13.04.11")

            .. doctest:: enigma_print_operation

                >>> cfg = EnigmaConfig.config_enigma("B-I-III-I", "EMO", "UX.MO.AY", "13.04.11") # doctest: +SKIP
                >>> cfg.print_operation(format='single', steps=10, show_step=True)
                0000      CNAUJVQSLEMIKBZRGPHXDFYTWO  EMO  19 10 05
                0001      UNXKGVERLYDIQBTWMHZOAFPCJS  EMP  19 10 06
                0002      QTYJZXUPKDIMLSWHAVNBGROFCE  EMQ  19 10 07
                0003      DMXAPTRWKYINBLUESGQFOZHCJV  ENR  19 11 08
                0004      IUSMHRPEAQTVDYWGJFCKBLOZNX  ENS  19 11 09
                0005      WMVXQRLSPYOGBTKIEFHNZCADJU  ENT  19 11 10
                0006      WKIQXNRSCVBOYFLUDGHZPJAEMT  ENU  19 11 11
                0007      RVPTWSLKYXHGNMQCOAFDZBEJIU  ENV  19 11 12
                0008      IYTKRVSMALDJHZWXUEGCQFOPBN  ENW  19 11 13
                0009      PSWGMODULZVIERFAXNBYHKCQTJ  ENX  19 11 14
                0010      IVOWZKHGARFSPUCMXJLYNBDQTE  ENY  19 11 15

            Show the operation of a machine as it encodes a message, with step numbers:

            .. doctest:: enigma_print_operation

                >>> cfg.print_operation(format='single', message='TESTING', show_step=True)
                0000      CNAUJVQSLEMIKBZRGPHXDFYTWO  EMO  19 10 05
                0001  T > UNXKGVERLYDIQBTWMHZO̲̅AFPCJS  EMP  19 10 06
                0002  E > QTYJZ̲̅XUPKDIMLSWHAVNBGROFCE  EMQ  19 10 07
                0003  S > DMXAPTRWKYINBLUESGQ̲̅FOZHCJV  ENR  19 11 08
                0004  T > IUSMHRPEAQTVDYWGJFCK̲̅BLOZNX  ENS  19 11 09
                0005  I > WMVXQRLSP̲̅YOGBTKIEFHNZCADJU  ENT  19 11 10
                0006  N > WKIQXNRSCVBOYF̲̅LUDGHZPJAEMT  ENU  19 11 11
                0007  G > RVPTWSL̲̅KYXHGNMQCOAFDZBEJIU  ENV  19 11 12

            Show the same process, but just what the operator would see:

            .. doctest:: enigma_print_operation

                >>> cfg.print_operation(format='windows', message='TESTING', show_encoding=True, show_step=True)
                0000  EMO
                0001  EMP  T > O
                0002  EMQ  E > Z
                0003  ENR  S > Q
                0004  ENS  T > K
                0005  ENT  I > P
                0006  ENU  N > F
                0007  ENV  G > L

            Show detailed internal version of the same process:

            .. doctest:: enigma_print_operation

                >>> cfg.print_operation(format='internal', message='TESTING', show_step=True) # doctest: +ELLIPSIS
                0000
                    ABCDEFGHIJKLMNOPQRSTUVWXYZ
                  P YBCDEFGHIJKLONMPQRSTXVWUAZ         UX.MO.AY
                  1 HCZMRVJPKSUDTQOLWEXNYFAGIB  O  05  I
                  2 KOMQEPVZNXRBDLJHFSUWYACTGI  M  10  III
                  3 AXIQJZKRMSUNTOLYDHVBWEGPFC  E  19  I
                  R YRUHQSLDPXNGOKMIEBFZCWVJAT         B
                  3 ATZQVYWRCEGOILNXDHJMKSUBPF         I
                  2 VLWMEQYPZOANCIBFDKRXSGTJUH         III
                  1 WZBLRVXAYGIPDTOHNEJMKFQSUC         I
                  P YBCDEFGHIJKLONMPQRSTXVWUAZ         UX.MO.AY
                    CNAUJVQSLEMIKBZRGPHXDFYTWO
                <BLANKLINE>
                0001
                T > ABCDEFGHIJKLMNOPQRST̲̅UVWXYZ
                  P YBCDEFGHIJKLONMPQRST̲̅XVWUAZ         UX.MO.AY
                  1 BYLQUIOJRTCSPNKVDWMX̲̅EZFHAG  P  06  I
                  2 KOMQEPVZNXRBDLJHFSUWYACT̲̅GI  M  10  III
                  3 AXIQJZKRMSUNTOLYDHVB̲̅WEGPFC  E  19  I
                  R YR̲̅UHQSLDPXNGOKMIEBFZCWVJAT         B
                  3 ATZQVYWRCEGOILNXDH̲̅JMKSUBPF         I
                  2 VLWMEQYP̲̅ZOANCIBFDKRXSGTJUH         III
                  1 YAKQUWZXFHOCSNGM̲̅DILJEPRTBV         I
                  P YBCDEFGHIJKLO̲̅NMPQRSTXVWUAZ         UX.MO.AY
                O < UNXKGVERLYDIQBTWMHZO̲̅AFPCJS
                <BLANKLINE>
                0002
                E > ABCDE̲̅FGHIJKLMNOPQRSTUVWXYZ
                  P YBCDE̲̅FGHIJKLONMPQRSTXVWUAZ         UX.MO.AY
                  1 XKPTH̲̅NIQSBROMJUCVLWDYEGZFA  Q  07  I
                  2 KOMQEPVZ̲̅NXRBDLJHFSUWYACTGI  M  10  III
                  3 AXIQJZKRMSUNTOLYDHVBWEGPFC̲̅  E  19  I
                  R YRU̲̅HQSLDPXNGOKMIEBFZCWVJAT         B
                ...

        """
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
            This function has been removed; use `print_operation` instead.
        """
        self.print_operation(message, format='internal', mark_func=mark_func)

    @staticmethod
    @require_unicode('msg')
    def _postprocess(msg):
        return '\n'.join(chunk_of(' '.join(chunk_of(msg, 4)), 60))

    @require_unicode('message')
    def print_encoding(self, message):
        """Show the conventionally formatted encoding of a message.

        Print out the encoding of a message by an (initial) `EnigmaConfig`, formatted into conventional
        blocks of four characters.

        Args:
            message (unicode): A message to encode. Characters that are not letters will be replaced with
                standard *Kriegsmarine* substitutions or be removed (see `make_message`).

        Examples:

            .. testsetup:: enigma_print_encoding

                cfg = EnigmaConfig.config_enigma("c-β-V-VI-VIII".decode("UTF-8"), u"CDTJ", u"AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", u"05.16.05.12")

            .. doctest:: enigma_print_encoding

                >>> cfg = EnigmaConfig.config_enigma("c-β-V-VI-VIII", "CDTJ", "AE.BF.CM.DQ.HU.JN.LX.PR.SZ.VW", "05.16.05.12") # doctest: +SKIP
                >>> cfg.print_encoding("FOLGENDES IST SOFORT BEKANNTZUGEBEN")
                RBBF PMHP HGCZ XTDY GAHG UFXG EWKB LKGJ

        """
        print(EnigmaConfig._postprocess(self.enigma_encoding(EnigmaConfig.make_message(message))))


# TBD - Tidy printing code so that the structures and names in config_string_internal and config_string match <<<
# TBD - Check spacing of lines, esp at end in .._string and print_... methods <<<
# ASK - Idiom for printing loops?
# REV - Keep list(reverse( conversions as [::-1] throughout?
