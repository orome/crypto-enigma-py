#!/usr/bin/env python
# encoding: utf8

# Copyright (C) 2016 by Roy Levien.
# This file is part of crypto-enigma, an Enigma Machine simulator.
# released under the BSD-3 License (see LICENSE.txt).

"""
This is a supporting module that defines the components used to construct an Enigma machine.
It will not generally be used directly.
"""

#from __future__ import (absolute_import, print_function, division, unicode_literals)
from typing import *
from enum import Enum

from itertools import cycle, islice
#from cachetools import cached

from .cypher import *
from functools import reduce


# REV - Additional performance improvements
# A note on the use of caching (cachetools):
# A large speed improvement comes from caching the encodings of rotors when first computed for a given position.
# This is effective because upper rotors don't change frequently so such cached mappings are reused many times.
# And because even the lower rotors will assume a maximum of 26 distinct positions, the cache will always be small.


LETTERS: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Direction(Enum):
    """The direction that a signal flows through a component.

    During encoding of a character, the signal passes first through the wiring of each `Component`,
    from right to left in the machine, in a forward (`~Direction.FWD`) direction, then through the reflector,
    and then, from left to right, through each component again, in reverse (`~Direction.REV`).
    This direction affects the encoding performed by the component (see `mapping`).
    """
    FWD = 1
    REV = 2


class Component(object):
    """A component of an Enigma machine.

    A component used to construct an Enigma machine (as embodied in an `~.machine.EnigmaConfig`) identified by
    its specification (see `name`), and characterized by its physical `wiring` and additionally — for rotors other
    than the reflector — by `turnovers` which govern the stepping (see `~.machine.EnigmaConfig.step`)
    of the machine in which it is installed.
    """

    # REV - Have this raise a more infomative error if used? -- http://stackoverflow.com/a/26025786/656912
    def __init__(self, name: str, wiring: str, turnovers: str):
        """
        There is no reason to construct a component directly, and no directly instantiated component
        can  be used in an `~.machine.EnigmaConfig`. The properties of components
        "outside of" an `~.machine.EnigmaConfig` can be :ref:`examined using <component_getting>` `component`.
        """
        # Should never happen if correct constructor has been used.
        assert name not in list(_comps.keys())

        self._name = name
        self._wiring = Mapping(wiring)
        self._turnovers = turnovers

    @property
    def name(self) -> str:
        """The specification a component of an Enigma machine.

        For rotors (including the reflector) this is one of the conventional letter or Roman numeral designations
        (e.g., `'IV'` or `'β'`) or rotor "names".
        For the plugboard this is the conventional string of letter pairs, indicating letters wired together
        by plugging (e.g., `'AU.ZM.ZL.RQ'`). Absence or non-use of a plugboard can be indicated with `'~'`
        (or almost anything that isn't a valid plugboard spec).

        Returns:
            str: A string uniquely specifying a `Component`.

        """
        return self._name

    @property
    def wiring(self) -> Mapping:
        """The physical wiring of a component, expressed as a |mapping|.

        Returns:
            Mapping: The `mapping` established by the physical wiring of a `Component`:
                the forward mapping when **01** is at the window position for rotors;
                by the plug arrangement for the plugboard.

        Examples:
            A rotor's wiring is fixed by the physical connections of the wires inside the rotor:

            >>> cmp = component('V')
            >>> cmp.wiring
            'VZBRGITYUPSDNHLXAWMJQOFECK'
            >>> component('VI').wiring
            'JPGVOUMFYQBENHZRDKASXLICTW'

            For plugboards, it is established by the specified connections:

            >>> component('AZ.BY').wiring
            'ZYCDEFGHIJKLMNOPQRSTUVWXBA'

        """
        return self._wiring

    @property
    def turnovers(self) -> str:
        """The turnover positions for a rotor.

        Returns:
            str: The letters on a rotor's ring that appear at the window (see `~.machine.EnigmaConfig.windows`)
                when the ring is in the turnover position.
                Not applicable (and empty) for the plugboard and for reflectors.
                (See `~.machine.EnigmaConfig.step`.)

        Examples:
            Only "full-width" rotors have turnovers:

            >>> component('V').turnovers
            'Z'
            >>> component('VI').turnovers
            'ZM'
            >>> component('I').turnovers
            'Q'

            Reflectors, "half-width" rotors, and the plugboard never do:

            >>> component('B').turnovers
            ''
            >>> component('β').turnovers
            ''
            >>> component('AG.OI.LM.ER.KU').turnovers
            ''


        """
        return self._turnovers

    # Caching here is essential; see general note on caching.
    #@cached({})
    def mapping(self, position: int, direction: Direction = Direction.FWD) -> str:
        """The mapping performed by a component based on its rotational position.

        The |mapping| performed by a `Component` as a function of its position (see `~.machine.EnigmaConfig.positions`)
        in an Enigma machine and the `Direction` of the signal passing through it.

        For all other positions of rotors, the mapping is a cyclic permutation this wiring's inputs (backward)
        and outputs (forward) by the rotational offset of the rotor away from the **01** position.

        Args:
            position (int): The rotational offset of the `Component` in the Enigma machine.
            direction (Direction): The direction of signal passage through the component.

        Returns:
            Mapping: The |mapping| performed by the component in the `direction` when `position` is
                at the window position.

        Examples:
            Note that because the wiring of reflectors generates mappings that consist entirely of paired exchanges
            of letters, reflectors (at any position) produce the same mapping in both directions (the same is true
            of the plugboard):

            >>> all(c.mapping(p, Direction.FWD) == c.mapping(p, Direction.REV) for c in map(component, reflectors) for p in range(1,26))
            True

        For rotors in their base position, with **01** at the window position, and for the plugboard,
        this is just the `wiring`:

        >>> cmp.wiring == cmp.mapping(1, Direction.FWD)
        True

        """

        assert direction in [Direction.FWD, Direction.REV]

        # REV - Smarter handling of edge cases and bounds?
        def rot_map(mp, st):
            st %= 26
            return list(islice(cycle(mp), st, 26 + st))

        steps = position - 1

        if direction == Direction.REV:
            return Mapping(''.join([chr_A0(p) for p in ordering(self.mapping(position, Direction.FWD))]))
        else:
            return Mapping(''.join([rot_map(LETTERS, -steps)[num_A0(c)] for c in rot_map(self._wiring, steps)]))

    def __str__(self) -> str:
        return "{0} {1} {2}".format(self._name, self._wiring, self._turnovers)

    # def __str__(self):
    #     return str(self).encode('utf-8')


# REV - Better way to initialize and store these as constants? <<<
_comps: Dict[str, Component] = dict()

# Rotors
_rots: Dict[str, Component] = dict()
_comps['I'] = _rots['I'] = Component('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
_comps['II'] = _rots['II'] = Component('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
_comps['III'] = _rots['III'] = Component('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')
_comps['IV'] = _rots['IV'] = Component('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
_comps['V'] = _rots['V'] = Component('V', 'VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
_comps['VI'] = _rots['VI'] = Component('VI', 'JPGVOUMFYQBENHZRDKASXLICTW', 'ZM')
_comps['VII'] = _rots['VII'] = Component('VII', 'NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM')
_comps['VIII'] = _rots['VIII'] = Component('VIII', 'FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM')
# Thin Naval rotors
_comps['β'] = _rots['β'] = Component('β', 'LEYJVCNIXWPBQMDRTAKZGFUHOS', '')
_comps['γ'] = _rots['γ'] = Component('γ', 'FSOKANUERHMBTIYCWLQPZXVGJD', '')

# Reflectors
_refs: Dict[str, Component] = dict()
_comps['A'] = _refs['A'] = Component('A', 'EJMZALYXVBWFCRQUONTSPIKHGD', '')
_comps['B'] = _refs['B'] = Component('B', 'YRUHQSLDPXNGOKMIEBFZCWVJAT', '')
_comps['C'] = _refs['C'] = Component('C', 'FVPJIAOYEDRZXWGCTKUQSBNMHL', '')
# Thin Naval reflctors
_comps['b'] = _refs['b'] = Component('b', 'ENKQAUYWJICOPBLMDXZVFTHRGS', '')
_comps['c'] = _refs['c'] = Component('c', 'RDOBJNTKVEHMLFCWZAXGYIPSUQ', '')

# The (standard) keyboard as a "component", for reference
_kbd: Dict[str, Component] = dict()
_comps[''] = _kbd[''] = Component('', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '')


# REV - Make these into Enums?
#: The list of valid (non-reflector) rotor names.
#:
#: >>> rotors # doctest: +SKIP
#: ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'β', 'γ']
rotors: List[str] = sorted(_rots.keys())

#: The list of valid reflector rotor names
#:
#: >>> reflectors
#: ['A', 'B', 'C', 'b', 'c']
reflectors: List[str] = sorted(_refs.keys())


#@require_unicode('name')
def component(name: str) -> Component:
    """Retrieve a specified component.

    Args:
        name: The `name` of a `Component`

    Returns:
        Component: The component with the specified name.

    Examples:
        Components are displayed as a string consisting of their properties:

        >>> print(component('VI'))
        VI JPGVOUMFYQBENHZRDKASXLICTW ZM

        Components with the same `name` are always identical:

        >>> component('AG.OI.LM.ER.KU') is component('AG.OI.LM.ER.KU')
        True

    """
    def plug(letters, swap):
        if len(swap) == 2 and swap[0] in LETTERS and swap[1] in letters:
            return [swap[0] if c == swap[1] else swap[1] if c == swap[0] else c for c in letters]
        else:
            return letters

    if name not in list(_comps.keys()):
        _comps[name] = Component(name, ''.join(reduce(plug, name.split('.'), list(LETTERS))), '')
    assert sorted(_comps[name].wiring) == list(LETTERS)
    assert all([t in _comps[name].wiring for t in _comps[name].turnovers])
    return _comps[name]